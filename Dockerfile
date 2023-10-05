# Referred from https://github.com/mmz-001/knowledge_gpt

FROM python:3.10-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \ 
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.5.1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/* 

COPY / ./

RUN pip install -r requirements.txt

EXPOSE 9900

CMD ["sh", "-c", "sleep 120 && python app.py"]
