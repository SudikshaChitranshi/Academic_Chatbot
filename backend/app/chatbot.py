
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

from app.intents import detect_intent
from app.tools import get_tool_response
from app.jsjiit_integration import handle_jsjiit_queries
from app.services.jiit_services import JIITService
from app.logger import log_response
import traceback

# Load LLM
llm = OllamaLLM(model="llama3.2:3b")

# JIIT-specific system prompt
jiit_system_prompt = """
You are a helpful assistant built specifically for students of Jaypee Institute of Information Technology (JIIT), Noida.
All questions are about JIIT unless explicitly stated otherwise.

You can answer queries about:
- JIIT faculty details (email, phone, cabin)
- Academic deadlines, events, subjects, clubs
- Student portal data like GPA, course registrations,attendance or fees

If something isn't found, politely suggest checking the official JIIT portal.
"""

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", jiit_system_prompt),
    ("human", "{input}")
])
chain = prompt | llm  # Connect prompt to model

# Main function for chatbot use

def get_bot_response(message: str,session=None):
    intent = detect_intent(message)

    # 1. Handle static tool-based responses
    if intent in ["faculty_info", "event_query", "syllabus", "assignment_due"]:
        tool_reply = get_tool_response(message, intent, session)
        log_response(message, tool_reply, source="Web Tool")
        return tool_reply, intent  


    # 2. Handle dynamic student data via JSJIIT
    if intent in ["courses_registered", "fees_due", "attendance", "student_marks", "student_gpa"]:
        if not session or "enrollment" not in session:
            return "🔐 Please log in to access this information."

        creds = session
        jiit_service = JIITService(creds["enrollment"], creds["password"])
        
        try:
            jsjiit_response = handle_jsjiit_queries(intent, jiit_service, message, session=session)
            if jsjiit_response:
                log_response(message, jsjiit_response, source="JSJIIT")
                return jsjiit_response, intent
        except Exception as e:
            error_trace = traceback.format_exc()
            log_response(message, str(e), source="JSJIIT Error")
            print("JSJIIT Exception:", error_trace)
            return "There was an issue fetching your data from the JIIT portal."
        else:
            return "Login to JIIT portal failed. Please check credentials."
    

    # 3. Fallback: LLM response
    try:
        llm_reply = chain.invoke({"input": message})
        print("LLM reply:", llm_reply)
        log_response(message, llm_reply, source="LLM")
        return str(llm_reply), intent
    except Exception as e:
        print("LLM ERROR:", e)
        return "Sorry, I encountered an issue processing your message.", intent
    