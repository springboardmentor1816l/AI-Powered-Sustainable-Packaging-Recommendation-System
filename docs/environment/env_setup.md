🌱 Environment & Tooling Setup Guide

This document explains how to set up the development environment for the AI-Powered Sustainable Packaging Recommendation System using:

Python virtual environment

Docker containers (backend + PostgreSQL + pgAdmin)

Common commands and checklist

1️⃣ Python Virtual Environment Setup
Step 1 — Create Virtual Environment
python -m venv venv

Step 2 — Activate Environment

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

Step 3 — Install Dependencies
pip install -r requirements.txt

Step 4 — Freeze Dependencies
pip freeze > requirements.txt


This ensures every team member uses the same versions.

2️⃣ Docker Setup

Docker allows the backend, database, and tools to run consistently in all systems.

2.1 Dockerfile

Create a file /environments/Dockerfile:

FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

2.2 docker-compose.yml

Create /environments/docker-compose.yml:

version: '3.9'
services:
  backend:
    build: .
    container_name: eco_backend
    ports:
      - "8000:8000"
    volumes:
      - ../src:/app/src
    depends_on:
      - db

  db:
    image: postgres:14
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
      POSTGRES_DB: ecopackdb
    ports:
      - "5432:5432"

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"

3️⃣ Repository Structure
/environments
   ├── Dockerfile
   ├── docker-compose.yml
   ├── requirements.txt

/src
/docs
   └── env_setup.md
/scripts

4️⃣ How to Run Docker
Build + Start containers
docker-compose up --build

Stop containers
docker-compose down