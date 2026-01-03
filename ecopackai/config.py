import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "ecopackai-secret")
    API_KEY = os.getenv("API_KEY", "ECO123")
