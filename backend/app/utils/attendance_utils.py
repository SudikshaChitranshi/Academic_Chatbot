# backend/app/utils/attendance_utils.py

def find_subject_attendance(all_attendance, user_query: str):
    user_query = user_query.lower()

    for sem_data in all_attendance:
        subjects = sem_data.get("studentattendancelist", [])
        for subject in subjects:
            subject_name = subject.get("subjectcode", "").lower()
            if user_query in subject_name:
                # Try to determine which component (L/P/T) has attendance
                total_classes = (
                    subject.get("Ltotalclass")
                    or subject.get("Ptotalclass")
                    or subject.get("Ttotalclass")
                )
                attended_classes = (
                    subject.get("Ltotalpres")
                    or subject.get("Ptotalpres")
                    or subject.get("Ttotalpres")
                )
                percentage = (
                    subject.get("LTpercantage")
                    or subject.get("Lpercentage")
                    or subject.get("Ppercentage")
                    or subject.get("Tpercentage")
                )

                return {
                    "subject": subject.get("subjectcode"),
                    "total": total_classes,
                    "attended": attended_classes,
                    "percentage": percentage
                }

    return None