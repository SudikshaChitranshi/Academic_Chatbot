# backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.chatbot import get_bot_response
from app.logger import log_response  # ✅ import the logger

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "Backend working!"}

@app.post("/api/chat")
async def chat_endpoint(req: Request):
    data = await req.json()
    user_msg = data.get("message", "")

    if not user_msg.strip():
        return {"reply": "Please enter a valid message."}
    
    result = get_bot_response(user_msg)
    if isinstance(result, tuple):
        bot_reply, _ = result
    else:
        bot_reply = result
    
    # ✅ Log the conversation
    log_response(user_message=user_msg, response=bot_reply, source="API")

    return {"reply": bot_reply}
