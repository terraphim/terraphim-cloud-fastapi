import json
import requests
import sys
if len(sys.argv)>1:
    server_url = sys.argv[1]
else:
    server_url = "https://alexmikhalev.terraphim.cloud/article/"

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
    r = requests.post(server_url, json = article)
    print(f"Created article {article['title']} with ID {r.text}")

with open('project_manager_CV.json', encoding='utf-8') as f:
    articles = json.loads(f.read(),strict=False)

for article in articles:
    print(article)
    r = requests.post(server_url, json = article)
    print(f"Created article {article['title']} with ID {r.text}")