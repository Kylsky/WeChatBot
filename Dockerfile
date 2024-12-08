FROM python:3.12-slim

ENV LANG=C.UTF-8 TZ=Asia/Shanghai

LABEL maintainer="kylsky"

RUN apt-get update && apt-get install -y --fix-missing \
    wget \
    curl \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install -U pip && pip install -r requirements.txt

COPY . .

RUN mkdir /app/logs/

CMD ["python", "/app/main.py"]

