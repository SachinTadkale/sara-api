import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
CHAT_MODEL = os.getenv("CHAT_MODEL")
BASE_URL = os.getenv("BASE_URL")

if not GROQ_API_KEY:
    RuntimeError("GROQ_API_KEY is not configured")
if not CHAT_MODEL:
    RuntimeError("CHAT_MODEL is not configured")
if not BASE_URL:
    RuntimeError("BASE_URL is not configured")