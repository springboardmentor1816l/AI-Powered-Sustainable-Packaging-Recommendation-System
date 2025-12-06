# EcoPackAI — Environment & Tooling Setup Guide

## 1. Create Python Virtual Environment
Choose your OS:

### Windows
```
python -m venv venv
venv\Scripts\activate
```

### Mac / Linux

```
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies
`pip install -r environments/requirements.txt`

### Freeze versions
`pip freeze > environments/requirements.txt`

---

# Note:
- Create `.env` (local, do NOT commit)
- Copy template: `cp .env.example .env`
- Edit `.env` with secure values (your DB password, pgAdmin password, SECRET_KEY etc.)

- Docker Compose reads `.env`
- It pulls variables into container envs so the backend can pick them up.


## 2. Docker Setup

### Install Docker
- Windows: Docker Desktop  
- Mac: Docker Desktop  
- Linux: Docker Engine  

---

## 3. Build & Run Containers

### Start all services (backend, DB, pgAdmin)
`docker-compose -f environments/docker-compose.yml up --build`

### Stop containers
`docker-compose -f environments/docker-compose.yml down`

---

## Folder Structure
```
/environments
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

/backend
/docs
/scripts
```

---

## Validation Checklist

- [x] Virtual environment successfully created  
- [x] Dependencies installed & frozen  
- [x] Dockerfile builds the backend image  
- [x] docker-compose starts backend + PostgreSQL + pgAdmin  
- [x] Environment is reproducible across machines  

This completes the Environment & Tooling Setup module.
