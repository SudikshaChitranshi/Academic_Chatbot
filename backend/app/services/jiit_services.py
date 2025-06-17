# backend/app/services/jiit_service.py

from pyjiit.wrapper import Webportal
from pyjiit.default import CAPTCHA
from pyjiit.attendance import AttendanceHeader

class JIITService:
    def __init__(self, enrollment_no: str, password: str):
        self.portal = Webportal()
        self.session = self.portal.student_login(enrollment_no, password, CAPTCHA)

    def get_registered_courses(self):
        semesters = self.portal.get_registered_semesters()
        if not semesters:
            return "No semesters found."

        registrations = self.portal.get_registered_subjects_and_faculties(semesters[-1])  # latest sem
        return registrations.subjects if registrations.subjects else "No registered subjects found."

    def get_attendance(self):
        semesters = self.portal.get_registered_semesters()
        all_data = []
        if not semesters:
            return "No semesters found."
        meta = self.portal.get_attendance_meta()
        header = AttendanceHeader(
        branchdesc=getattr(meta, "branchdesc", "Unknown Branch"),
        name=getattr(meta, "name", "Unknown Name"),
        programdesc=getattr(meta, "programdesc", "Unknown Program"),
        stynumber=getattr(meta, "stynumber", "000")
    )

        for sem in semesters:
            try:
                attendance = self.portal.get_attendance(header, sem)
                if attendance:
                    all_data.append({
                    "semester": sem,
                    "studentattendancelist": attendance.get("studentattendancelist", [])
                })
            except Exception as e:
                print(f"⚠️ Error fetching attendance for {sem}: {e}")
        return all_data if all_data else "No attendance data available."
    
    def get_fees(self):
        return "No fees information available at the moment."
    
    def get_gpa(self):
        return "GPA details not available yet."
