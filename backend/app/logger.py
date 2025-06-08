import json
from datetime import datetime

def log_chat(user_id, message, reply, intent):
    log = {
        "user_id": user_id,
        "timestamp": str(datetime.now()),
        "message": message,
        "reply": reply,
        "intent": intent
    }
    try:
        with open("app/chat_logs.json", "r+") as f:
            data = json.load(f)
            data.append(log)
            f.seek(0)
            json.dump(data, f, indent=2)
    except FileNotFoundError:
        with open("app/chat_logs.json", "w") as f:
            json.dump([log], f, indent=2)
