FROM python:3-alpine3.8
COPY requirements.txt .

ENV TERRAFORM_VERSION=1.2.2

RUN apk -U add gcc musl-dev libffi-dev openssl-dev docker curl git zip unzip wget

RUN cd /tmp && \
    curl -sSLO https://releases.hashicorp.com/terraform/$TERRAFORM_VERSION/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
        unzip terraform_*_linux_amd64.zip -d /usr/bin && \
    rm -rf /tmp/* && \
    rm -rf /var/tmp/*

ENV PYTHONDONTWRITEBYTECODE donot

RUN pip install --no-cache-dir -r requirements.txt
ADD infra /infra
