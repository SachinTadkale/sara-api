from fastapi import APIRouter
from app.services.newsService import get_hacker_news
news_router = APIRouter()

@news_router.get("/hacker_news")
def get_latest_news():
    return get_hacker_news()
