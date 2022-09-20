from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection
from models import Article
import json 

from typing import Optional
from pydantic import BaseModel

#TODO turn it into redis cache keymiss
class SearchQuery(BaseModel):
    search: str
    skip: Optional[int] = None
    limit: Optional[int] = None

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



import os 
redis = get_redis_connection()
user = os.getenv('USER','default')
def read_default_config():
    with open('./defaults/desktop_config.json') as f:
        return json.load(f)

@app.post("/article/new")
def create_article(article: Article):
    return article.save()

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/search")
def get_search(search:str, skip: int = 0, limit: int = 10):
    articles = Article.find(Article.body % search).all()
    return articles

@app.post("/search")
async def search(search:SearchQuery):
    articles = Article.find(Article.body % search.search).all()
    return articles

@app.get("/config")
async def config():
    config_str=redis.json().get("user:{user}:config")
    if not config_str:
        return jsonable_encoder(read_default_config())
    else:
        return {config_str}
