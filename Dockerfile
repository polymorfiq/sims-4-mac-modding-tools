FROM python:alpine3.10

RUN apk add --update --no-cache bash g++ gcc libxslt-dev zip
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV PATH="/app/bin:${PATH}"

COPY . .
