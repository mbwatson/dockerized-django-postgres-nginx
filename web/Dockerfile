FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /web
COPY . /web
WORKDIR /web

RUN pip install -r requirements.txt
