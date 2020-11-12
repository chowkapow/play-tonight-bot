FROM python:3.8-slim

ENV ENV=prod
# Enables container logs
ENV PYTHONUNBUFFERED=1
# Fix docker build on Raspberry Pi
ENV MULTIDICT_NO_EXTENSIONS=1
ENV YARL_NO_EXTENSIONS=1

WORKDIR /bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY /src ./src
COPY .env ./.env

CMD python3 src/play-tonight-bot.py $ENV
