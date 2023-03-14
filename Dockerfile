FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN chmod +x ./wait-for-it.sh

RUN pip3 install -r requirements.txt