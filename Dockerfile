FROM python:3
MAINTAINER jherrlin@gmail.com

ENV PYTHONUNBUFFERED 1

RUN apt-get update -qq && \
    apt-get install -y build-essential imagemagick libmagickwand-dev libmagickcore-dev gettext

ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

RUN mkdir /logs && \
    touch /logs/all.log && \
    pip install -r requirements.txt
