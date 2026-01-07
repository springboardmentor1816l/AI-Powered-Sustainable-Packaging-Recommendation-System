# EcoPackAI 🌱

AI-powered sustainable packaging recommendation system.

## Features
- Cost prediction using Random Forest
- CO₂ emission prediction using XGBoost
- Material ranking logic
- Explainable AI (feature importance)
- Flask REST API
- PostgreSQL integration
- Docker-ready

## Project Structure

## API Endpoints
- `GET /health` → Health check
- `GET /materials` → List materials
- `POST /predict` → Predict cost & CO₂

## Run Locally
```bash
python -m api.app
