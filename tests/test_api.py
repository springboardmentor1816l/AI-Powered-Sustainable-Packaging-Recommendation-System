import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app import app

def test_health():
    """Test health check endpoint"""
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "UP"

def test_predict_missing_data():
    """Test predict endpoint with missing required fields"""
    client = app.test_client()
    response = client.post("/predict", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Missing required field" in data["error"]

def test_predict_invalid_category():
    """Test predict endpoint with invalid category"""
    client = app.test_client()
    payload = {
        "product_name": "Test Product",
        "product_weight_kg": 1.0,
        "category": "InvalidCategory",
        "fragility_index": 0.5,
        "shipping_type": "Air"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_predict_valid_request():
    """Test predict endpoint with valid data"""
    client = app.test_client()
    payload = {
        "product_name": "Test Product",
        "product_weight_kg": 2.0,
        "category": "Food",
        "fragility_index": 0.5,
        "shipping_type": "Road"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "predictions" in data
    assert len(data["predictions"]) > 0
    assert "status" in data
    assert data["status"] == "success"
