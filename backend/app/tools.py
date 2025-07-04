from duckduckgo_search import DDGS
from app.logger import log_response
import os
import json

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
  
    elif intent in ["online_course_recommendation", "study_resource"]:
        return web_search_tool(f"{msg} site:youtube.com OR site:coursera.org OR site:geeksforgeeks.org")

    else:
        response = web_search_tool(msg)
        log_response(msg, response, source="Web Tool")
        return response


