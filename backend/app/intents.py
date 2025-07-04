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
    else:
        return "web_query"


