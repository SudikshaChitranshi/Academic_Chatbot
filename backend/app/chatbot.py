
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from app.intents import detect_intent
from app.tools import get_tool_response
from app.logger import log_response

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

    # 2. LLM response
    try:
        llm_reply = chain.invoke({"input": message})
        print("LLM reply:", llm_reply)
        log_response(message, llm_reply, source="LLM")
        return str(llm_reply), intent
    except Exception as e:
        print("LLM ERROR:", e)
        return "Sorry, I encountered an issue processing your message.", intent
    