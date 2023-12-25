FROM ubuntu:latest
FROM python:3.10

LABEL authors="lenguyen"

ARG GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_PORT=${GRADIO_SERVER_PORT}

WORKDIR /

COPY . .


RUN pip install -r ./requirements.txt

EXPOSE 7860

#CMD ["python", "app.py"]

