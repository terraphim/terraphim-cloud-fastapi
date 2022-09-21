# terraphim-cloud-fastapi
FastAPI python and Redis OM backend for Terraphim Cloud 
```
docker compose up 
```
create venv or conda env, install requirements, then:
```
uvicorn main:app --reload
```
API documentation available on 
```
http://127.0.0.1:8000/redoc
```
and `http://127.0.0.1:8000/docs`

populate with test data via data /data/dataloader.py

