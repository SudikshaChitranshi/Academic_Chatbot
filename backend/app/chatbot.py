from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_ollama import OllamaLLM
from app.tools import get_tool_response
from app.intents import detect_intent

llm = OllamaLLM(model="llama3:8b")

jiit_system_prompt = """
You are a helpful assistant built specifically for students of Jaypee Institute of Information Technology (JIIT), Noida.
All questions are about JIIT unless explicitly stated otherwise.

Answer with reliable and up-to-date information about:
- JIIT faculty (email, cabin, phone)
- JIIT events, clubs, projects
- Academic deadlines, tests, assignments
- JIIT-specific resources (notes, quizzes, previous year papers)

If the user doesn't mention JIIT, still assume they mean JIIT-related queries.
"""
# Create prompt template chain
prompt = ChatPromptTemplate.from_messages([
    ("system", jiit_system_prompt),
    ("human", "{input}")
])
chain = prompt | llm  # Connect prompt to model

def get_bot_response(message: str):
    intent = detect_intent(message)

    if intent in ["faculty_info", "event_query", "syllabus", "assignment_due"]:
        tool_reply = get_tool_response(message, intent)
        return tool_reply, intent
    else:
        llm_reply = chain.invoke({"input": message})
        return llm_reply.content, intent
