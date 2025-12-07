# Environment & Tooling Setup Guide

This document explains how to set up the Python virtual environment and Docker environment for the project.

---

## 1. Python Virtual Environment Setup

### Step 1: Create a Virtual Environment

#### Windows:
python -m venv venv
venv\Scripts\activate

#### Mac/Linux:
python3 -m venv venv
source venv/bin/activate

---

## Step 2: Install Required Packages
All Python dependencies are listed in:
environments/requirements.txt

Install them using:
pip install -r environments/requirements.txt

---

## Step 3: Freeze Installed Packages
This updates the requirements file with the correct versions.

pip freeze > environments/requirements.txt

---

## 2. Docker Setup

### Step 1: Build and Start Containers
Run the following inside the environments folder:

docker-compose up --build

This will start:
- Backend service  
- PostgreSQL database  
- pgAdmin interface  

---

### Step 2: Stop Containers

docker-compose down

---

## 3. Project Folder Structure

/environments  
    Dockerfile  
    docker-compose.yml  
    requirements.txt  

/docs  
    env_setup.md  

/src  
    (backend source code)

---

## 4. Useful Commands

Deactivate virtual environment:
deactivate

Check running docker containers:
docker ps

Rebuild docker containers:
docker-compose up --build

Stop containers:
docker-compose down

---

## 5. Validation Checklist

✔ Virtual environment created  
✔ requirements.txt updated  
✔ Dockerfile added  
✔ docker-compose.yml added  
✔ env_setup.md created  
✔ Project runs successfully with `docker-compose up --build`  
✔ venv folder NOT uploaded to GitHub  
