import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app import app

def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200

def test_predict_unauthorized():
    client = app.test_client()
    response = client.post("/predict", json={})
    assert response.status_code == 401
