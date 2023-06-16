import json
import requests
server_url = "https://alexmikhalev.terraphim.cloud:8443/article/new"
with open('ref_arch.json', encoding='utf-8') as f:
    articles = json.loads(f.read())

for article in articles:
    r = requests.post(server_url, json = article)
    print(f"Created article {article['title']}")

with open('attacking_ml.json', encoding='utf-8') as f:
    articles = json.loads(f.read(),strict=False)

for article in articles:
    print(article)
    r = requests.post(server_url, json = article)
    print(f"Created article {article['title']} with ID {r.text}")

with open('org_project.json', encoding='utf-8') as f:
    articles = json.loads(f.read(),strict=False)

for article in articles:
    print(article)
    r = requests.post('https://alexmikhalev.terraphim.cloud:8443/article/new', json = article)
    print(f"Created article {article['title']} with ID {r.text}")
