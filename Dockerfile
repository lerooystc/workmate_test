FROM python:3.12.4-slim-bullseye

WORKDIR /usr/src/project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./core ./core
COPY ./tests ./tests
COPY ./pyproject.toml .

RUN adduser --disabled-password --gecos '' myuser
