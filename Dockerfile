FROM alpine:latest

RUN apk add --no-cache python3-dev \
    && pip install --upgrade pip