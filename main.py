from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
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
import os 
redis = get_redis_connection()
user = os.getenv('USER','default')
def read_default_config():
    with open('./defaults/default_config.json') as f:
        config=json.load(f)
    return config

@app.route("/article/new", methods=["POST"])
def create_article():
    try:
        print(request.json)
        new_article = Article(**request.json)
        new_article.save()
        return new_article.pk

    except ValidationError as e:
        print(e)
        return "Bad request.", 400


@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/search")
async def get_search(search:str, skip: int = 0, limit: int = 10):
    return {"message": f"Hello search {search}"}

@app.post("/search")
async def search(search:SearchQuery):
    return search

@app.get("/config")
async def config():
    config_str=redis.json().get("user:{user}:config")
    if not config_str:
        return {"config":jsonable_encoder(read_default_config())}
    else:
        return {"config":config_str}
