import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "logs", "chat_logs.txt")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_response(user_message: str, response: str, source: str = "LLM"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = (
        f"[{timestamp}] [SOURCE: {source}]\n"
        f"User: {user_message}\n"
        f"Bot: {response}\n\n"
    )
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)

