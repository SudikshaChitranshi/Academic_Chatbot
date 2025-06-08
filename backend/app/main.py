from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.chatbot import get_bot_response
from app.logger import log_chat

app = FastAPI()

# CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInput(BaseModel):
    message: str
    user_id: str

@app.post("/chat")
async def chat_endpoint(payload: ChatInput):
    reply, intent = get_bot_response(payload.message)
    log_chat(payload.user_id, payload.message, reply, intent)
    return {"response": reply, "intent": intent}
