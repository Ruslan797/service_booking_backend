FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements-docker.txt ./
RUN pip install --upgrade pip && pip install -r requirements-docker.txt


COPY . .
