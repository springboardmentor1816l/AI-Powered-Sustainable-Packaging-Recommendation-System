FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ backend/
COPY ml/ ml/

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["python", "-m", "backend.app"]

