FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY backend /app/backend
COPY worker /app/worker
COPY frontend /app/frontend
COPY scripts /app/scripts
COPY .env.example /app/.env.example

EXPOSE 8501 8000 8001

CMD ["python", "scripts/start_all.py"]
