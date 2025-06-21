# backend/app/main.py
from fastapi import FastAPI, Request
from app.routes import cgpa_route
from fastapi.middleware.cors import CORSMiddleware
from app.chatbot import get_bot_response
from app.logger import log_response  

app = FastAPI()
app.include_router(cgpa_route.router)
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
    session = data.get("session", {})   

    if not user_msg.strip():
        return {"reply": "Please enter a valid message."}
    
    result = get_bot_response(user_msg, session=session)
    if isinstance(result, tuple):
        bot_reply, _ = result
    else:
        bot_reply = result
    
    # ✅ Log the conversation
    log_response(user_message=user_msg, response=bot_reply, source="API")

    return {"reply": bot_reply}
