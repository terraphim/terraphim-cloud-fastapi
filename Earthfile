VERSION 0.7
PROJECT applied-knowledge-systems/terraphim-cloud-fastapi
FROM ubuntu:18.04
IMPORT ./frontend-svelte AS frontend

ci-pipeline:
  PIPELINE
  TRIGGER push main
  TRIGGER pr main
  BUILD +release

build-fastapi:
  FROM ghcr.io/applied-knowledge-systems/redismod:bionic
  RUN apt remove python-pip
  RUN apt install -y python3-pip
  RUN apt-get install -y python3-venv
  RUN apt-get install -y python3.8-minimal python3.8-dev python3.8-venv
  RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 10
  RUN python3.8 -m pip install pip
  WORKDIR /fastapiapp
  COPY --dir defaults .
  COPY main.py models.py requirements.txt .
  RUN python3.8 -m venv ./venv_terraphim_cloud
  RUN /fastapiapp/venv_terraphim_cloud/bin/python3.8 -m pip install -U pip
  RUN /fastapiapp/venv_terraphim_cloud/bin/python3.8 -m pip install -r /fastapiapp/requirements.txt
  SAVE ARTIFACT /fastapiapp /fastapiapp

release:
  FROM ghcr.io/applied-knowledge-systems/redismod:bionic
  WORKDIR /fastapiapp
  COPY +build-fastapi/fastapiapp .
  COPY frontend+build/dist/assets ./assets
  COPY frontend+build/dist/index.html ./assets/index.html
  SAVE IMAGE --push ghcr.io/applied-knowledge-systems/terraphim-fastapiapp:bionic