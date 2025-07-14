
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from app.intents import detect_intent
from app.tools import get_tool_response
from app.logger import log_response
from app.knowledge import get_knowledge_response

# Load LLM
llm = OllamaLLM(model="llama3.2:3b")

# JIIT-specific system prompt
jiit_system_prompt = """
You are a helpful AI assistant for students at Jaypee Institute of Information Technology (JIIT), Noida.

You specialize in answering questions related to:
- JIIT academics, faculty, deadlines, events, clubs, etc.
- Common academic topics such as computer science, engineering, management, and campus life.

Always prioritize giving direct and informative answers. If a question is about JIIT, respond with JIIT-specific information. If it is a general academic or technical query, answer it directly without assuming it must relate to JIIT.

Avoid suggesting that a question is outside your scope unless it is unrelated to academics or student life.
# """

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
    
    # 2. Search knowledge.json first
    kb_reply = get_knowledge_response(message)
    if kb_reply:
        log_response(message, kb_reply, source="Knowledge Base")
        return kb_reply, intent


    # 3. Fallback LLM response
    try:
        llm_reply = chain.invoke({"input": message})
        log_response(message, llm_reply, source="LLM")
        return str(llm_reply), intent
    except Exception as e:
        print("LLM ERROR:", e)
        return "Sorry, I encountered an issue processing your message.", intent
    