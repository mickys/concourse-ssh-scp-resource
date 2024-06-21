FROM python:3.12.4-alpine3.20

RUN apk add --no-cache openssh

COPY src/* /opt/resource/
