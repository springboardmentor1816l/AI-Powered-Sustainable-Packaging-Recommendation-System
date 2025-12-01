# EcoPackAI — Sustainable Packaging Recommendation Platform

EcoPackAI predicts cost efficiency & carbon footprint of packaging materials and recommends optimal eco-friendly options.

## Features
- AI-powered recommendation engine
- CO₂ and cost analytics dashboard
- Full-stack architecture: Flask, PostgreSQL, Bootstrap, ML models
- Deployment-ready cloud architecture

## Repo Layout
See folders: `backend/`, `frontend/`, `ml/`, `dashboard/`, `docs/`, `tests/`, `.github/workflows/`

## Quickstart (dev)
1. Create virtualenv: `python -m venv .venv && source .venv/bin/activate`
2. Install: `pip install -r requirements.txt`
3. Run backend: `python backend/app.py`

## Core Endpoints (planned)
- `POST /api/recommend` — input product details, returns ranked packaging options
- `GET  /api/health` — health check

## Deliverables (Kickoff)
- docs/architecture_diagram.png
- README v1
- CI pipeline stub `.github/workflows/ci.yml`
- Module skeletons
