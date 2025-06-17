# backend/app/__init__.py

from .chatbot import get_bot_response
from .tools import get_tool_response
from .intents import detect_intent
from .services.jiit_services import JIITService
