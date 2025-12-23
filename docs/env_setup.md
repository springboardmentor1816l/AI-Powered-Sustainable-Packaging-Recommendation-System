📄 env_setup.md — Environment & Tooling Setup Guide
🧩 EcoPackAI — Environment Setup Guide

This guide explains how to set up the full development environment, including Python virtual environment, Docker, PostgreSQL, and pgAdmin.

✔ 1. Prerequisites
Install the following tools:

Python 3.11+

Docker Desktop (latest version)

VS Code

Git

Make sure Docker Desktop is running before starting.

✔ 2. Project Folder Structure
AI-Powered-Sustainable-Packaging-Recommendation-System/
│
├── backend/
├── dashboard/
├── frontend/
├── ml/
├── tests/
│
├── environments/
│     ├── Dockerfile
│     ├── docker-compose.yml
│     ├── requirements.txt            (Full local dev requirements)
│     └── backend-requirements.txt    (Only backend dependencies for Docker)
│
├── docs/
│     └── env_setup.md   ← (this file)
│
└── venv/                 (Python virtual environment)

✔ 3. Setup Python Virtual Environment (Local Development)
Create venv:
python -m venv venv

Activate (Windows):
venv\Scripts\activate


You should now see:

(venv)

Install full development requirements:
pip install -r environments/requirements.txt

Freeze updated dependencies (optional):
pip freeze > environments/requirements.txt

✔ 4. Docker Setup (Backend + PostgreSQL + pgAdmin)

Docker uses a minimal set of dependencies stored in:

environments/backend-requirements.txt

Build the Docker containers:
cd environments
docker compose build

Start all services:
docker compose up

Stop containers:
docker compose down

✔ 5. Accessing the Backend

After containers start successfully:

FastAPI Backend
http://localhost:8000

FastAPI API Documentation (Swagger UI)
http://localhost:8000/docs

✔ 6. Accessing PostgreSQL & pgAdmin
Open pgAdmin:
http://localhost:5050

Login Credentials:

Email: admin@ecopackai.com

Password: admin123

✔ 7. Connecting pgAdmin to PostgreSQL
Add New Server → Fill details:

General Tab → Name

ecopack-db


Connection Tab:

Field	Value
Hostname	db
Port	5432
Username	postgres
Password	postgres
Maintenance DB	ecopackai_db

Click Save.

If connection is successful, you will see:

Servers → ecopack-db → Databases → ecopackai_db

✔ 8. Running Backend from Docker

Docker automatically starts your backend using:

uvicorn backend.main:app --host 0.0.0.0 --port 8000


Logs can be viewed in Docker Desktop under the backend container.

✔ 9. Troubleshooting
❌ Docker not recognized

Install Docker Desktop + enable WSL2.

❌ pgAdmin cannot connect to db

Check these:

Containers running (docker compose ps)

Hostname is exactly db

Password is postgres

❌ Backend fails to start

Check backend logs in Docker Desktop.