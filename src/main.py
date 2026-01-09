# src/main.py
from fastapi import FastAPI
from src.inference.analytics import analytics_bp
app.register_blueprint(analytics_bp)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello — app is running!"}
