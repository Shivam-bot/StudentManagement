FROM python:3.8

ENV PYTHONBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./venv.txt /app/venv.txt

RUN pip install -r venv.txt

COPY . /app

