from openai import OpenAI
from app.config.settings import GROQ_API_KEY,BASE_URL

client = OpenAI(
    api_key= GROQ_API_KEY,
    base_url= BASE_URL
)
