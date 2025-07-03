# backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.chatbot import get_bot_response
from app.logger import log_response  
from app.services.jiit_services import JIITService
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


@app.post("/api/attendance")
async def get_attendance_for_semester(req: Request):
    data = await req.json()
    session = data.get("session")
    semester_id = data.get("semester_id")

    if not session or not semester_id:
        return {"error": "Missing data"}

    jiit = JIITService(session["enrollment"], session["password"])
    meta = jiit.portal.get_attendance_meta()

    # Find the correct semester object
    semester = next((sem for sem in meta.semesters if sem.registration_id == semester_id), None)
    if semester is None:
        return {"error": "Semester not found"}

    header = meta.headers[0]  # default header
    attendance = jiit.portal.get_attendance(header, semester)

    return [
        {
            "subject": sub["subjectname"],
            "total": sub["totaldelivered"],
            "attended": sub["totalattended"],
            "percent": sub["percentage"]
        }
        for sub in attendance["studentattendancelist"]
    ]