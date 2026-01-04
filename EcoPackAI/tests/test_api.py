import json
from src.app import app

def test_health():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200

def test_predict_unauthorized():
    client = app.test_client()
    res = client.post("/predict", json={})
    assert res.status_code == 401
