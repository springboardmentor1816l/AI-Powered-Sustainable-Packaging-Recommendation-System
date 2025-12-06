# === EcoPackAI Backend Dockerfile ===
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional but recommended)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application
COPY ../backend /app

# Expose backend port
EXPOSE 5000

# Run Flask backend
CMD ["python", "app.py"]
