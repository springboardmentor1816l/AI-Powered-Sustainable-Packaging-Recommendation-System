FROM python:3.11-slim
WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

# copy requirements from the environments folder
COPY environments/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy source code from project root src/
COPY src/ ./src

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
