def detect_intent(message: str) -> str:
    message = message.lower()

    if any(keyword in message for keyword in ["faculty", "email", "phone", "cabin"]):
        return "faculty_info"
    elif any(keyword in message for keyword in ["event", "club", "hackathon", "competition"]):
        return "event_query"
    elif any(keyword in message for keyword in ["assignment", "due date", "deadline"]):
        return "assignment_due"
    elif any(keyword in message for keyword in ["syllabus", "course outline"]):
        return "syllabus"
    elif any(keyword in message for keyword in ["gpa", "grades", "cgpa","sgpa"]):
        return "student_gpa"
    elif any(keyword in message for keyword in ["marks"]):
        return "student_marks"
    elif any(keyword in message for keyword in ["registered courses", "next semester"]):
        return "courses_registered"
    elif any(keyword in message for keyword in ["attendance"]):
        return "attendance"
    elif any(keyword in message for keyword in ["fees", "dues", "payment"]):
        return "fees_due"
    else:
        return "web_query"


