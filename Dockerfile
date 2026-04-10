FROM docker.m.daocloud.io/library/python:3.11-slim

WORKDIR /code/docker

COPY ./requirements.txt /code/docker/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/docker/requirements.txt

COPY ./ /code/docker

CMD ["fastapi", "run", "./main.py", "--port", "80"]