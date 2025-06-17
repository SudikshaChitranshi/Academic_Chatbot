# app/pyjiit_integration.py

from app.services.jiit_services import JIITService
from app.utils.attendance_utils import find_subject_attendance
import re, string
import os
from dotenv import load_dotenv

load_dotenv()

# Load credentials from .env
enrollment = os.getenv("JIIT_ENROLLMENT")
password = os.getenv("JIIT_PASSWORD")

if not enrollment or not password:
    raise ValueError("Missing JIIT_ENROLLMENT or JIIT_PASSWORD in .env file")

# Create a single instance
try:
    jiit_service = JIITService(enrollment, password)
except Exception as e:
    jiit_service = None
    print(f"[ERROR] Failed to initialize JIITService: {e}")

def handle_pyjiit_queries(intent, jiit_service, user_query=""):
    if intent == "student_gpa":
        return f"Your current GPA is: {jiit_service.get_gpa()}"
    elif intent == "courses_registered":
        courses = jiit_service.get_registered_courses()
        return "You're registered for the following courses:\n" + "\n".join(courses)
    elif intent == "attendance":
        all_attendance = jiit_service.get_attendance()
        query = re.sub(r"(what\s+is\s+)?(my\s+)?attendance\s+(in|for)", "", user_query.strip().lower()).strip()
        query = query.translate(str.maketrans("", "", string.punctuation)).strip()

        for sem in all_attendance:
            for subj in sem.get("studentattendancelist", []):
                subj_name = subj.get("subjectcode", "").lower()
                if query in subj_name:  # fuzzy contains-match
                    percentage = (
                        subj.get("LTpercantage")
                        or subj.get("Lpercentage")
                        or subj.get("Ppercentage")
                        or subj.get("Tpercentage")
                        or "N/A"
                    )
                    attended = (
                        subj.get("Ltotalpres")
                        or subj.get("Ptotalpres")
                        or subj.get("Ttotalpres")
                        or 0
                    )
                    total = (
                        subj.get("Ltotalclass")
                        or subj.get("Ptotalclass")
                        or subj.get("Ttotalclass")
                        or 0
                    )

                    return (
                        f"**Attendance for `{subj['subjectcode']}`**:\n"
                        f"• **Total Classes:** `{total}`\n"
                        f"• **Attended:** `{attended}`\n"
                        f"• **Percentage:** `{percentage}`%"
                    )

        return "⚠️ No attendance data found for that subject."

    elif intent == "fees_due":
        return f"Your outstanding fee details: {jiit_service.get_fees()}"
    else:
        return None

