def detect_intent(msg):
    msg = msg.lower()
    if "syllabus" in msg:
        return "get_syllabus"
    if "email" in msg or "contact" in msg:
        return "faculty_contact"
    if "resource" in msg or "material" in msg:
        return "study_resources"
    if any(keyword in msg for keyword in ["admission", "faculty", "jiit", "placement", "deadline"]):
        return "web_query"
    return None
