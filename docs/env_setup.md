# Environment Setup Guide

## 1. Virtual Environment Setup (Local Development)
To run the project locally without Docker:

### Create Environment
```bash
# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

# Environment Setup Guide

## How to Run with Docker
1. **Prerequisite:** Ensure Docker Desktop is running.
2. **Navigate:** Go to the environments folder: `cd environments`
3. **Start:** Run `docker-compose up --build`
4. **Access:**
   - Backend API: http://localhost:5000
   - pgAdmin (DB Viewer): http://localhost:5050

## How to Stop
- Press `Ctrl+C` in the terminal.
- Run `docker-compose down` to remove containers.