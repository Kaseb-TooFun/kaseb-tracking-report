FROM python:3.8.3-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && gcc python3-dev

ENV LIBRARY_PATH=/lib:/usr/lib

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN yes yes | ./manage.py collectstatic

EXPOSE 8000
ENTRYPOINT python manage.py migrate && \
    hypercorn server.asgi:application --bind 0.0.0.0:8000