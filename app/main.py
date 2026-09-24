from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.AiRouter import router 
from app.routers.newsRouter import news_router
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "http://localhost:4200",
        "http://localhost:4300",
    ],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
app.include_router(router)
app.include_router(news_router)

@app.get('/')
def health():
    return 'AI APIs are running '