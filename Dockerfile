FROM python:alpine3.10

RUN apk add --update --no-cache bash g++ gcc libxslt-dev zip git make
RUN git clone https://github.com/rocky/python-decompile3.git && cd python-decompile3 && git checkout 2af0305fbbc9faf677bd8ef8ab7d4c87045026cc && make install

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV PATH="/app/bin::${PATH}"

COPY . .
