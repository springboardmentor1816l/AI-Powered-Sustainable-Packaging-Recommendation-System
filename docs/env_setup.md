# EcoPackAI — Environment & Tooling Setup Guide

This guide explains how to set up the development environment using:
- Python virtual environment
- Docker
- Docker Compose

---

## 1. Python Virtual Environment Setup

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r environments/requirements.txt
pip freeze > environments/requirements.txt
