# backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.chatbot import get_bot_response
from app.logger import log_response  
from app.services.jiit_services import JIITService
from pyjiit.exceptions import APIError
from io import BytesIO
import pymupdf
from app.MarksExtractor import parse_report
from app.elective_api import get_recommendations_from_csv
import time

app = FastAPI()

origins = [
    "http://localhost:5173",  # Your frontend URL
    "http://localhost:5000",  # Add other allowed origins as needed
]
# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "Backend working!"}

@app.post("/api/chat")
async def chat_endpoint(req: Request):
    start = time.time()
    data = await req.json()
    user_msg = data.get("message", "")
    session = data.get("session", {})   

    if not user_msg.strip():
        return {"reply": "Please enter a valid message."}
    
    result = get_bot_response(user_msg, session=session)
    print("⏱️ get_bot_response took:", time.time() - start, "sec")
    if isinstance(result, tuple):
        bot_reply, _ = result
    else:
        bot_reply = result
    
    # ✅ Log the conversation
    log_response(user_message=user_msg, response=bot_reply, source="API")

    return {"reply": bot_reply}

@app.post("/api/recommend")
async def recommend(request: Request):
    data = await request.json()
    # Expect fields: student_id, name, branch, semester, cgpa, preferences, taken_courses
    student_data = {
        "Student ID": data["student_id"],
        "Name": data["name"],
        "Branch": data["branch"],
        "Semester": data["semester"],
        "CGPA": data["cgpa"],
        "Preferences": data["preferences"],
        "Courses_taken_ids": ';'.join(data["taken_courses"]),
        "Courses_taken": data["taken_courses"]
    }
    try:
        result = get_recommendations_from_csv(student_data)
        return { "recommendations": result }
    except Exception as e:
        return { "error": str(e) }
    

@app.post("/api/semesters/attendance")
async def get_attendance_semesters(req: Request):
    data = await req.json()
    session = data.get("session", {})
    if not session:
        return {"error": "Missing session"}

    jiit = JIITService(session["enrollment"], session["password"])
    meta = jiit.portal.get_attendance_meta()

    return [
        {
            "registration_id": sem.registration_id,
            "registration_code": sem.registration_code
        }
        for sem in meta.semesters
    ]

@app.post("/api/semesters/marks")
async def get_marks_semesters(req: Request):
    data = await req.json()
    session = data.get("session", {})
    if not session:
        return {"error": "Missing session"}

    jiit = JIITService(session["enrollment"], session["password"])
    
    try:
        semesters = jiit.portal.get_semesters_for_marks()
    except Exception as e:
        return {"error": str(e)}
    
    return [
        {
            "registration_id": sem.registration_id,
            "registration_code": sem.registration_code,
            "label": sem.registration_code  # optional for dropdown labels
        }
        for sem in semesters
    ]

@app.post("/api/attendance")
async def get_attendance_for_semester(req: Request):
    data = await req.json()
    session = data.get("session", {})
    semester_id = data.get("semester_id")

    if not session or not semester_id:
        return {"error": "Missing session or semester_id"}

    jiit = JIITService(session["enrollment"], session["password"])

    # Step 1: Get meta data (headers + semesters)
    meta = jiit.portal.get_attendance_meta()
    header = meta.headers[0]  # Usually there's only one
    semester = next((s for s in meta.semesters if s.registration_id == semester_id), None)

    if semester is None:
        return {"error": "Invalid semester selected."}

    # Step 2: Get attendance
    try:
        attendance_data = jiit.portal.get_attendance(header, semester)
        print(attendance_data)
        if not attendance_data.get("studentattendancelist"):
            return {"message": "⚠️ No attendance records found for this semester."}
    except APIError as e:
        if "NO Attendance Found" in str(e):
            return {"message": "⚠️ No attendance available for this semester yet."}
        raise e  

    result = []
    for sub in attendance_data.get("studentattendancelist", []):
        subject = sub.get("subjectcode")
        percent = (
            sub.get("LTpercantage")
            or sub.get("Lpercentage")
            or sub.get("Ppercentage")
            or sub.get("Tpercentage")
            or "N/A"
        )
        attended = (
            sub.get("Ltotalpres")
            or sub.get("Ptotalpres")
            or sub.get("Ttotalpres")
            or 0
        )
        total = (
            sub.get("Ltotalclass")
            or sub.get("Ptotalclass")
            or sub.get("Ttotalclass")
            or 0
        )

        result.append({
            "subject": subject,
            "attended": attended,
            "total": total,
            "percent": percent,
        })
    return result

@app.post("/api/marks")
async def get_marks(req: Request):
    data = await req.json()
    session = data.get("session", {})
    student = data.get("student", {})

    if not session:
        return {"error": "Missing session"}
    if not student:
        return {"error": "Missing student"}

    jiit = JIITService(session["enrollment"], session["password"])

    try:
        # Step 1: Download the marks PDF from the portal
        pdf_bytes = jiit.portal.get_marks_pdf(student)  # <-- you'll define this

        # Step 2: Parse the PDF from bytes
        doc = pymupdf.open(stream=BytesIO(pdf_bytes), filetype="pdf")
        parsed = parse_report(doc)

        return parsed  # return as JSON to frontend
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/gpa")
async def get_gpa(req: Request):
    data = await req.json()
    session = data.get("session")

    if not session:
        return {"error": "Missing session"}

    try:
        jiit = JIITService(session["enrollment"], session["password"])
        gpa_data = jiit.get_gpa()

        return {
            "reply": gpa_data["summary"],      # React shows this
            "graph_data": gpa_data["graph_data"]  # React plots this
        }

    except Exception as e:
        return {
            "error": f"Failed to fetch GPA: {str(e)}"
        }
