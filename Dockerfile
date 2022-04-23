FROM python:3.8-alpine

MAINTAINER Mikhail Knyazev "Knyazev9art@yandex.ru"

RUN adduser -D wishlist

WORKDIR /home/wishlist

RUN apk add dos2unix
RUN python -m venv venv
COPY requirements.txt ./
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY instance instance
COPY .flaskenv manage.py config.py boot.sh ./

RUN dos2unix ./boot.sh
RUN chmod +x boot.sh

ENV FLASK_APP manage.py

RUN chown -R wishlist:wishlist ./
USER wishlist

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]

