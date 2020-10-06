FROM python:3.8-slim

ENV ENV=dev
ENV PYTHONUNBUFFERED=1

WORKDIR /bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY /src ./src
COPY .env ./.env

CMD python3 src/play-tonight-bot.py $ENV
