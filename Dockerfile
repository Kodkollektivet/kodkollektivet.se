FROM python:3
MAINTAINER jherrlin@gmail.com

ENV PYTHONUNBUFFERED 1
ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

RUN mkdir /logs && \
    touch /logs/all.log && \
    pip install -r requirements.txt
