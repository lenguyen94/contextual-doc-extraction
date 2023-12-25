FROM ubuntu:latest
FROM python:3.10

LABEL authors="lenguyen"

WORKDIR /

COPY ./requirements.txt .

COPY . .

RUN --mount=type=cache,target=/root/.cache/pip pip install -r ./requirements.txt

EXPOSE 8000

#CMD ["uvicorn", "main:app"]

