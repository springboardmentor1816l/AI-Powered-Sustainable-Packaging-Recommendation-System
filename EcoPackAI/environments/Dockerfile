# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY ../src/ ./src

# Set entrypoint (example: FastAPI backend)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
