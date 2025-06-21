# app/pyjiit_integration.py

from app.services.jiit_services import JIITService
import asyncio
from app.services.jsjiit_client import get_cgpa_sgpa
import re, string


def handle_pyjiit_queries(intent, jiit_service, user_query="",session=None):

    if intent == "courses_registered":
        if not session or "enrollment" not in session:
            return "🔐 Please log in to view your registered courses."
        courses = jiit_service.get_registered_courses()
        return "You're registered for the following courses:\n" + "\n".join(courses)
    
    elif intent == "attendance":
        if not session or "enrollment" not in session:
            return "🔐 Please log in to view your attendance."
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

