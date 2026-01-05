import pytest
import json
from app import app, db
from models.database import PredictionHistory

@pytest.fixture
def client():
    # Configure app for testing mode
    app.config['TESTING'] = True
    # Use an in-memory database to avoid touching your real ecopack.db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all() # Create clean tables for every test
        yield client

# 1. TEST: Health Check Endpoint
def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'

# 2. TEST: Security Middleware (Unauthorized Access)
def test_predict_unauthorized(client):
    # Sending a request WITHOUT the X-API-KEY header
    response = client.post('/predict', json={
        "product_weight_kg": 1.5,
        "fragility_index": 0.3,
        "category": "Electronics"
    })
    assert response.status_code == 401
    assert "Unauthorized" in response.get_json()['error']

# 3. TEST: Successful Prediction & Persistence
def test_predict_success(client):
    headers = {'X-API-KEY': 'ecopack-secret-2026'}
    payload = {
        "product_weight_kg": 1.5,
        "fragility_index": 0.3,
        "category": "Electronics"
    }
    response = client.post('/predict', headers=headers, json=payload)
    
    # Check API response
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'predictions' in data
    
    # Check Database Persistence (Verify it actually saved)
    with app.app_context():
        record = PredictionHistory.query.first()
        assert record is not None
        assert record.product_weight_kg == 1.5