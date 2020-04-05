FROM alpine:latest

RUN apk add --no-cache python-dev \
    && pip install --upgrade pip