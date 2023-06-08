from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection
from models import Article
import json 
from fastapi.responses import FileResponse

from typing import Optional
from pydantic import BaseModel

#TODO turn it into redis cache keymiss
class SearchQuery(BaseModel):
    search: str
    skip: Optional[int] = None
    limit: Optional[int] = None
    role: Optional[str] = None

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets",html=True), name='assets')  
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# import os 
# config_switch=os.getenv('DOCKER', 'local')
# if config_switch=='local':
#FIXME: change config
cluster_host="127.0.0.1"
cluster_port=30001
host="127.0.0.1"
port=6379
# else:
#     cluster_host = "rgcluster"
#     cluster_port =  30001
#     host="redisgraph"
#     port=6379

redis = get_redis_connection(host=host,port=port, decode_responses=True)
from redis.cluster import RedisCluster

rediscluster_client = RedisCluster(host=cluster_host, port=cluster_port, decode_responses=True)
print(rediscluster_client.get_nodes())

import httpimport
with httpimport.remote_repo(['terraphim_utils'], "https://raw.githubusercontent.com/terraphim/terraphim-platform-automata/main/"):
    import terraphim_utils
from terraphim_utils import loadAutomata,find_matches

def load_matcher(url):
    Automata=loadAutomata(url)
    return Automata

def match_nodes(search_string, Automata):
    nodes=set()
    matched_ents=find_matches(search_string,Automata)
    nodes = set([node[0] for node in matched_ents])
    tags={term:id for id, term, _, _, in matched_ents}
    return list(nodes),tags

def get_edges(nodes, years=None, limits=400,mnodes=set()):
    """
    return all edges for the specified nodes, limit hardcoded
    """
    links=list()
    nodes_set=set()
    years_set=set()
    print(mnodes)
    print(limits)
    redis_graph = redis.graph('cord19medical')
    if years is not None:
        print("Graph query node params "+str(nodes))
        params = {'ids':nodes, 'years':years,'limits':int(limits)}
        query="""WITH $ids as ids MATCH (e:entity)-[r]->(t:entity) where (e.id in ids) and (r.year in $years) RETURN DISTINCT e.id, t.id, max(r.rank), r.year ORDER BY r.rank DESC LIMIT $limits"""
        
    else:
        params = {'ids':nodes,'limits':int(limits)}
        print("Graph query node params "+str(nodes))
        query="""WITH $ids as ids MATCH (e:entity)-[r]->(t:entity) where e.id in ids RETURN DISTINCT e.id, t.id, max(r.rank), r.year ORDER BY r.rank DESC LIMIT $limits"""
    print(query)
    result = redis_graph.query(query,params)
    for record in result.result_set:
        if record[0] not in mnodes:
            nodes_set.add(record[0])
        else:
            print(f"Node {record[0]} excluded")
        if record[1] not in mnodes:
            nodes_set.add(record[1])
        else:
            print(f"Node {record[1]} excluded")
        if record[3]:
            years_set.add(record[3])
        if (record[0] in mnodes) or (record[1] in mnodes):
            continue
        else: 
            links.append({'source':record[0],'target':record[1],'rank':record[2],'created_at':str(record[3])})
    return links, list(nodes_set), list(years_set)
    
user = os.getenv('USER','default')

def read_default_config():
    with open('./defaults/desktop_config.json') as f:
        return json.load(f)

@app.post("/article/new")
def create_article(article: Article):
    print(article.title)
    print(article.pk)
    redis.hset(f"article_id:{article.pk}",mapping={'title': article.title})
    redis.hset(f"article_id:{article.pk}",mapping={'url': article.url})
    body=' '.join(article.body.split('\n'))
    rediscluster_client.set(f"paragraphs:{article.pk}",body)
    rediscluster_client.sadd('processed_docs_stage1_para',article.pk)
    return article.save()

@app.get("/")
async def root():
    return FileResponse('assets/index.html', media_type='text/html')

@app.get("/search")
def get_search(search:str, skip: int = 0, limit: int = 10):
    articles = Article.find(Article.body % search).all()
    return articles

@app.post("/search")
async def search(search:SearchQuery):
    if not search.search:
        return []
    articles = Article.find(Article.body % search.search).all()
    return articles

@app.post("/rsearch")
async def search(search:SearchQuery):
    if search.role:
        role = search.role 
    else:
        role = "Default"
    print(f"Role {role}")
    config_str=redis.json().get("user:{user}:config")
    if not config_str:
        config_str=jsonable_encoder(read_default_config())

    Automata=load_matcher(config_str['roles'][role]['automata_url'])
    nodes, tags =match_nodes(search.search,Automata=Automata)
    print("Nodes")
    print(nodes)
    print("Matched tags")
    print(tags)
    links,_,_=get_edges(nodes,limits=50)
    print("Links")
    print(links)
    result_table=[]
    article_set=set()
    for each_record in links[0:50]:  
        edge_query=each_record['source']+":"+each_record['target'] 
        print(edge_query)
        edge_scored=redis.zrangebyscore(f"edges_scored:{edge_query}",'-inf','inf',0,5)
        print(edge_scored)
        if edge_scored:
            for sentence_key in edge_scored:
                *head,tail=sentence_key.split(':')
                article_id=head[1]
                if article_id not in article_set:
                    title=redis.hget(f"article_id:{article_id}",'title')
                    url=redis.hget(f"article_id:{article_id}",'url')
                    print(url)
                    print("body key",f"paragraphs:{article_id}")
                    body=rediscluster_client.get(f"paragraphs:{article_id}")
                    print("Description key",head)
                    description=rediscluster_client.hget(":".join(head),tail)
                    # print(f"Connected terms {hash_tags[each_record['source']]} {hash_tags[each_record['target']]}")
                    print("Connected terms ")
                    print(each_record['source'])
                    print(each_record['target'])
                    result_table.append({'title':title,'pk':article_id,'url': url,'body': body, 'description':description,"tags":tags,"connected_terms":[each_record['source'],each_record['target']]})
                    article_set.add(article_id)
        return result_table

@app.get("/config")
async def config():
    config_str=redis.json().get("user:{user}:config")
    if not config_str:
        return jsonable_encoder(read_default_config())
    else:
        return {config_str}
