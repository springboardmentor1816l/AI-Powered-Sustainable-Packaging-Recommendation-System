FROM python:3.11-slim

WORKDIR /app

# Copy requirements first
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend folder
COPY backend ./backend

EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


