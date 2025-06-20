FROM python:3.11.4-alpine3.17

RUN apk add --no-cache --upgrade bash

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONBUFFERED 1

EXPOSE 8000

COPY requirements.txt ./backend/requirements.txt
COPY backend ./backend

WORKDIR /backend

RUN python -m venv /venv

ENV PATH="/scripts:/venv/bin:$PATH"

RUN pip install --upgrade pip && \
 pip install -r requirements.txt && \
 chmod -R +x /backend/scripts/