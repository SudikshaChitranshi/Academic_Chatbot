from duckduckgo_search import DDGS
from app.services.jiit_services import JIITService
from app.pyjiit_integration import handle_pyjiit_queries
from app.logger import log_response
import os
import json
from app.services.jsjiit_client import get_cgpa_sgpa


CACHE_FILE = os.path.join(os.path.dirname(__file__), "data", "web_cache.json")
os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

# Load cache on startup
try:
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        web_cache = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    web_cache = {}

def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as file_handle:
        json.dump(web_cache, file_handle, indent=2)

def web_search_tool(query):
    if query in web_cache:
        return f"🔁 (Cached)\n{web_cache[query]}"

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=2)
        if not results:
            return "No relevant information found on the web."

        formatted = "\n".join([f"- {r['title']}: {r['href']}" for r in results])
        web_cache[query] = formatted
        save_cache()
        return formatted

def get_tool_response(msg, intent,session=None):
    if intent == "faculty_info":
        response = web_search_tool(f"site:jiit.ac.in {msg}")
        log_response(msg, response, source="Web Tool")
        return response

    elif intent == "syllabus_query":
        response = web_search_tool(f"syllabus {msg}")
        log_response(msg, response, source="Web Tool")
        return response

    elif intent == "event_info":
        response = web_search_tool(f"JIIT events {msg}")
        log_response(msg, response, source="Web Tool")
        return response

    elif intent in ["attendance", "courses_registered", "fees_due"]:
        if not session or "enrollment" not in session:
            return "🔒 Please login to access this information."
        
        creds = session
        jiit_service = JIITService(creds["enrollment"], creds["password"])
    
        response = handle_pyjiit_queries(intent,jiit_service, msg, session=session)
        log_response(msg, response, source="PyJIIT")
        return response
    
    elif intent == "student_gpa":
        if not session or "enrollment" not in session:
            return "🔒 Please login to fetch GPA."

        creds = session
        response = get_cgpa_sgpa(creds["enrollment"], creds["password"])
        log_response(msg, response, source="JSJIIT")
        return (
            f"🎓 Your CGPA is `{response['cgpa']}` and SGPA is `{response['sgpa']}`"
            if "cgpa" in response else f"⚠️ {response.get('error', 'Unable to fetch GPA.')}"
        )
    
    elif intent in ["online_course_recommendation", "study_resource"]:
        return web_search_tool(f"{msg} site:youtube.com OR site:coursera.org OR site:geeksforgeeks.org")

    else:
        response = web_search_tool(msg)
        log_response(msg, response, source="Web Tool")
        return response


