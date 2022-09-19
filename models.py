from redis_om import get_redis_connection, EmbeddedJsonModel, HashModel,JsonModel, Field, Migrator
import datetime
from typing import List 

class Person(EmbeddedJsonModel):
    first_name: str = Field(index=True, full_text_search=True)
    last_name: str = Field(index=True, full_text_search=True)
    email: str = Field(index=True, full_text_search=True)
    bio: str
    date_added: datetime.date = Field(default=datetime.datetime.now())


class Article(HashModel):
    title: str = Field(index=True, full_text_search=True)
    url: str = Field(index=True, full_text_search=True)
    body: str = Field(index=True, full_text_search=True)

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