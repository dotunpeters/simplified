FROM alpine:latest

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

RUN apk add install libxml2-dev libxslt-dev python-dev

RUN pip3 install python3-lxml

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt