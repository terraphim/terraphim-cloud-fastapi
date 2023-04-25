from redis_om import get_redis_connection, EmbeddedJsonModel, HashModel,JsonModel, Field, Migrator,NotFoundError
import datetime
from typing import List 

REDIS_DATA_URL = "redis://localhost:9001"

class Article(HashModel):
    title: str = Field(index=True, full_text_search=True)
    url: str = Field(index=True, full_text_search=True)
    body: str = Field(index=True, full_text_search=True)
    class Meta:
        database = get_redis_connection(url=REDIS_DATA_URL, decode_responses=True)

# class Article(JsonModel):
#     title: str = Field(index=True, full_text_search=True)
#     description: str = Field(index=True, full_text_search=True)
#     content: str = Field(index=True, full_text_search=True)
#     tags: List[str] = Field(index=True)
#     categories: List[str] = Field(index=True)
#     date_added: datetime.date = Field(
#         default=datetime.datetime.today().strftime("%Y-%m-%d")
#     )

Migrator().run()