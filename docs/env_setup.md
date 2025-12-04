Environment & Tooling Setup Guide
Overview

This document explains how to set up a standardized development environment using Python virtual environments, Docker, PostgreSQL, and pgAdmin. The goal is to ensure consistent, reproducible development environments for all team members.

Project Structure
/
│
├── .env
├── docs/
│   └── env_setup.md
│
├── environments/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
│
└── src/
    └── main.py

1. Python Virtual Environment Setup
Step 1 — Create virtual environment

Linux/macOS:

python3 -m venv .venv
source .venv/bin/activate


Windows:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

Step 2 — Install dependencies
pip install -r environments/requirements.txt

Step 3 — Freeze installed packages
pip freeze > environments/requirements.txt

2. Environment Variables (.env File)

Create a .env file in the project root with the following:

POSTGRES_USER=appuser
POSTGRES_PASSWORD=apppassword
POSTGRES_DB=appdb

PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=admin

DATABASE_URL=postgresql+psycopg2://appuser:apppassword@db:5432/appdb

3. Dockerfile (Backend Service)

Place this inside environments/Dockerfile:

FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY environments/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

4. docker-compose.yml (Multi-Service Setup)

Place this inside environments/docker-compose.yml:

version: "3.8"
services:
  backend:
    build:
      context: ..
      dockerfile: ./environments/Dockerfile
    container_name: backend
    ports:
      - "8000:8000"
    env_file:
      - ../.env
    depends_on:
      - db
    volumes:
      - ../src:/app/src
    restart: unless-stopped

  db:
    image: postgres:15
    container_name: postgres_db
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-appuser}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-apppassword}
      POSTGRES_DB: ${POSTGRES_DB:-appdb}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  pgadmin:
    image: dpage/pgadmin4:7
    container_name: pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL:-admin@example.com}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD:-admin}
    ports:
      - "8080:80"
    restart: unless-stopped

volumes:
  pgdata:

5. Starting Docker Environment

Open terminal and run:

cd environments
docker-compose up --build


To run in the background:

docker-compose up -d


To stop everything:

docker-compose down

6. Validating the Setup
Backend API

Open:

http://localhost:8000/


Expected:

{"message": "Hello — app is running!"}


API documentation:

http://localhost:8000/docs

pgAdmin

Open:

http://localhost:8080/


Login using:

Email: admin@example.com
Password: admin

Connecting pgAdmin to PostgreSQL

In pgAdmin:

Right-click "Servers"

Click "Create → Server"

Fill:

General:

Name: localdb


Connection:

Host: db
Port: 5432
Username: appuser
Password: apppassword
Database: appdb


Click "Save".

7. Troubleshooting

Backend logs:

docker-compose logs -f backend


Database logs:

docker-compose logs -f db


If ports are busy, change mapping in docker-compose.yml, e.g.:

"8001:8000"

8. Validation Checklist
Task	Status
Virtual environment created	✔
requirements.txt generated	✔
Dockerfile working	✔
docker-compose.yml working	✔
Backend accessible on port 8000	✔
FastAPI docs accessible	✔
PostgreSQL running	✔
pgAdmin running	✔
Database connected	✔
Environment reproducible	✔
End of env_setup.md