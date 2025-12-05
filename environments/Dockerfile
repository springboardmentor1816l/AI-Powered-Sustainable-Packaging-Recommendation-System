FROM python:3.10-slim

WORKDIR /app

# Copy requirements into container
COPY environments/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy full project
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
