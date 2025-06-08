from langchain_ollama import OllamaLLM
from app.tools import get_tool_response
from app.intents import detect_intent

llm = OllamaLLM(model="llama3:8b") # Or any local model like mistral


def get_bot_response(message: str):
    intent = detect_intent(message)

    if intent:
        tool_reply = get_tool_response(message, intent)
        return tool_reply, intent

    llm_reply = llm.invoke(message)
    return llm_reply, "general"
