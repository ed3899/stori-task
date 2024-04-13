FROM python:3.12.3-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r ./requirements.txt

COPY ./email_sender.py .
COPY ./transaction_processor.py .

ADD source dest