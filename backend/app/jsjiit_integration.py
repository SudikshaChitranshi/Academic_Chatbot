# app/jsjiit_integration.py

from app.services.jiit_services import JIITService
import re, string

def summarize_marks(grade_card, sem_code):
    if not grade_card or "subjectlist" not in grade_card:
        return f"No marks found for {sem_code}."

    lines = [f"📘 Marks for {sem_code}:"]
    for subject in grade_card["subjectlist"]:
        name = subject.get("subjectdesc", "Unnamed")
        grade = subject.get("grade", "N/A")
        lines.append(f"• {name}: {grade}")

    return "\n".join(lines)

def handle_jsjiit_queries(intent, jiit_service, user_query="",session=None):

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
    
    elif intent == "student_marks":
        if not session or "enrollment" not in session:
            return "🔐 Please log in to view your marks."
        try:
            semesters = jiit_service.portal.get_semesters_for_marks()
            if not semesters:
                return "No mark records found."
            latest_semester = semesters[-4]  # most recent semester
            print(latest_semester)
            grade_card = jiit_service.get_grade_card()
            print(grade_card)

            return summarize_marks(grade_card, latest_semester.registration_code)

        except Exception as e:
            return f"Error fetching semesters for marks: {e}"
        
    elif intent == "student_gpa":
        if not session or "enrollment" not in session:
            return "🔐 Please log in to view your gpa."
        try:
            gpa_result = jiit_service.get_gpa()
            return gpa_result["summary"], {"graph_data": gpa_result["graph_data"]}
        except Exception as e:
            return f"Error fetching GPA data: {e}"
    else:
        return None

