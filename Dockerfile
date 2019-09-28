FROM python:alpine3.10

RUN apk add bash
WORKDIR /app
COPY . .
