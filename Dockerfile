FROM python:alpine3.10

RUN apk add --update --no-cache bash g++ gcc libxslt-dev
WORKDIR /app
COPY tools/requirements.txt tools/requirements.txt
RUN pip install -r tools/requirements.txt

COPY . .
