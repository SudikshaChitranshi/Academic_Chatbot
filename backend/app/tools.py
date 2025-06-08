from duckduckgo_search import DDGS
import os, json


def load_json(filename):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "data", filename)
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def web_search_tool(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=2)
        if not results:
            return "No relevant information found on the web."
        return "\n".join([f"- {r['title']}: {r['href']}" for r in results])


def find_faculty(message):
    faculty_list = load_json("faculty.json").keys()
    for name in faculty_list:
        if name.lower() in message.lower():
            return name
    return None


def get_tool_response(msg, intent):
    if intent == "faculty_info":
        faculty_data = load_json("faculty.json")
        name = find_faculty(msg)
        if name and name in faculty_data:
            faculty = faculty_data[name]
            return (
                f"Name: {name}\n"
                f"Email: {faculty.get('email', 'N/A')}\n"
                f"Phone: {faculty.get('phone', 'N/A')}\n"
                f"Department: {faculty.get('department', 'N/A')}\n"
                f"Cabin: {faculty.get('cabin', 'N/A')}\n"
                f"Expertise: {', '.join(faculty.get('expertise', []))}"
            )
        else:
            # 🔁 Fallback to web search
            return web_search_tool(msg)

    elif intent == "syllabus_query":
        syllabus = load_json("syllabus.json")
        for subject, link in syllabus.items():
            if subject.lower() in msg.lower():
                return f"Syllabus for {subject}: {link}"
        return "Syllabus not found."

    elif intent == "event_info":
        return web_search_tool(msg)

    else:
        return web_search_tool(msg)
