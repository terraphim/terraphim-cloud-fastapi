from redis_om import get_redis_connection, EmbeddedJsonModel, HashModel,JsonModel, Field, Migrator,NotFoundError
import datetime
from typing import List, Optional

#FIXME: change to env variable
REDIS_DATA_URL = "redis://127.0.0.1:6379"
# host="127.0.0.1"
# port=6379


class Article(HashModel):
    title: str = Field(index=True, full_text_search=True)
    url: str = Field(index=True, full_text_search=True)
    body: str = Field(index=True, full_text_search=True)

    date_added: datetime.date = Field(
        default=datetime.datetime.today().strftime("%Y-%m-%d")
    )
    class Meta:
        database = get_redis_connection(url=REDIS_DATA_URL, decode_responses=True)

# class Article(JsonModel):
#     title: str = Field(index=True, full_text_search=True)
#     url: str = Field(index=True, full_text_search=True)
#     description: Optional[str] = Field(index=True, full_text_search=True)
#     body: str = Field(index=True, full_text_search=True)
#     tags: Optional[List[str]] = Field(index=True)
#     date_added: datetime.date = Field(
#         default=datetime.datetime.today().strftime("%Y-%m-%d")
#     )
#     class Meta:
#         database = get_redis_connection(url=REDIS_DATA_URL, decode_responses=True)

Migrator().run()