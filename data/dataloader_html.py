import json
import requests
import sys
import glob 
if len(sys.argv)>1:
    server_url = sys.argv[1]
else:
    server_url = "https://alexmikhalev.terraphim.cloud/article/"

for each_file in glob.glob("*.html"):
    with open(each_file, encoding='utf-8') as f:
        article = f.read()
        # print(article)
        json_object=json.dumps(article)
        with open(each_file+"json", "w") as outfile:
            outfile.write(json_object)

