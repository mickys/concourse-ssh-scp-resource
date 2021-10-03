FROM python:3.6.3-alpine3.6

RUN apk add --no-cache openssh

COPY src/* /opt/resource/
