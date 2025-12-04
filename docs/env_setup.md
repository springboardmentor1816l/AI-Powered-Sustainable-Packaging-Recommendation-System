# Environment Setup Guide — EcoPackAI

## 1. Python Virtual Environment Setup
### Create environment
python -m venv venv

### Activate environment
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

## 2. Install Dependencies
pip install -r environments/requirements.txt

## 3. Freeze Dependencies
pip freeze > environments/requirements.txt

## 4. Docker Setup
Install Docker Desktop:
https://www.docker.com/products/docker-desktop/

## 5. Build & Start Containers
cd environments
docker-compose up --build

## 6. Stop Containers
docker-compose down

## 7. Folder Structure
/environments
    Dockerfile
    docker-compose.yml
    requirements.txt
/docs
    env_setup.md
