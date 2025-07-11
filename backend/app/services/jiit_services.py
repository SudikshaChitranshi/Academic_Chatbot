# backend/app/services/jiit_service.py
from pyjiit.wrapper import Webportal
from pyjiit.default import CAPTCHA

def summarize_marks(grade_card, sem_code):
    if not grade_card or "subjectlist" not in grade_card:
        return f"No marks found for {sem_code}."

    lines = [f"📘 Marks for {sem_code}:"]
    for subject in grade_card["subjectlist"]:
        name = subject.get("subjectdesc", "Unnamed")
        grade = subject.get("grade", "N/A")
        lines.append(f"• {name}: {grade}")

    return "\n".join(lines)

def analyze_gpa_trend(semester_list):
        if not semester_list:
            return "No GPA data available.", []

        trend = []
        summary_data = []
        last_cgpa = None

        for sem in sorted(semester_list, key=lambda s: s["stynumber"]):
            sgpa = sem["sgpa"]
            cgpa = sem["cgpa"]
            sem_num = sem["stynumber"]
            summary_data.append((sem_num, sgpa, cgpa))

            if last_cgpa is not None:
                diff = round(cgpa - last_cgpa, 2)
                if diff > 0:
                    trend.append(f"📈 Semester {sem_num}: CGPA improved by {diff}")
                elif diff < 0:
                    trend.append(f"📉 Semester {sem_num}: CGPA dropped by {abs(diff)}")
                else:
                    trend.append(f"➖ Semester {sem_num}: CGPA unchanged")
            last_cgpa = cgpa

        return "\n".join(trend), summary_data

class JIITService:
    def __init__(self, enrollment_no: str, password: str):
        self.portal = Webportal()
        self.session = self.portal.student_login(enrollment_no, password, CAPTCHA)

    def get_grade_card(self):
        semesters = self.portal.get_semesters_for_grade_card()
        if not semesters:
            return "No semesters found."

        latest_semester = semesters[-1]
        respo = self.portal._get_program_id()
        print(respo)
        try:
            grade_card = self.portal.get_grades_card(latest_semester)
            return grade_card
        except Exception as e:
            return f"Error fetching grade card: {e}"

    def get_semesters_for_marks(self):
        try:
            semesters = self.portal.get_semesters_for_marks()
            if not semesters:
                return "No mark records found."
            latest_semester = semesters[0]  # most recent semester
            grade_card = self.portal.get_grades_card(latest_semester)

            return summarize_marks(grade_card, latest_semester.registration_code)
        except Exception as e:
            return f"Error fetching semesters for marks: {e}"
        

    def get_gpa(self):
        try:
            sgpa_cgpa = self.portal.get_sgpa_cgpa()
            semesters = sgpa_cgpa.get("semesterList", [])
            summary_text, summary_data = analyze_gpa_trend(semesters)

            return {
            "summary": summary_text,
            "graph_data": summary_data
            }

        except Exception as e:
         return {
            "summary": f"Error fetching GPA data: {e}",
            "graph_data": []
        }
