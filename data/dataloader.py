import json
import requests

# with open('ref_arch.json', encoding='utf-8') as f:
#     articles = json.loads(f.read())

# for article in articles:
#     r = requests.post('http://localhost:8000/article/new', json = article)
#     print(f"Created article {article['title']} with ID {r.text}")

with open('attacking_ml.json', encoding='utf-8') as f:
    articles = json.loads(f.read(),strict=False)

for article in articles:
    r = requests.post('http://localhost:8000/article/new', json = article)
    print(f"Created article {article['title']} with ID {r.text}")