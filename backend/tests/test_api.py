import json

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200

def test_predict_unauthorized(client):
    res = client.post("/predict", json={})
    assert res.status_code == 401
