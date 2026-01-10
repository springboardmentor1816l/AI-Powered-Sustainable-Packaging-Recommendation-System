# === EcoPackAI Backend Dockerfile ===
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project source into container
COPY . .

# Expose backend port
EXPOSE 5000

# Run Flask backend
CMD ["python", "app.py"]
