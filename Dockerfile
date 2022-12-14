FROM python:3.8-slim

ARG DEBIAN_FRONTEND noninteractive
ENV TZ America/Sao_Paulo

RUN apt-get update && apt-get install -y tzdata wget gnupg2 software-properties-common ca-certificates lsb-release

RUN apt-get clean autoclean && \
    apt-get autoremove --yes && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/ /var/cache/apt/archives

RUN mkdir -p /app/pyapp

WORKDIR /app

COPY requirements.txt /app/

RUN python -m venv .venv && \
    . .venv/bin/activate && \
    pip install -r requirements.txt


COPY ./pyapp /app/pyapp/
COPY ./start_app.sh /app/
COPY ./main.py /app/

CMD [ "sh" , "start_app.sh" ]