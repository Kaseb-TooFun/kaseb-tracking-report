FROM python:3.8.3-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add python3-dev

ENV LIBRARY_PATH=/lib:/usr/lib

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
#ARG SECRET_KEY
#ENV SECRET_KEY=$SECRET_KEY
ENTRYPOINT python manage.py migrate && \
    hypercorn server.asgi:application --bind 0.0.0.0:8000
