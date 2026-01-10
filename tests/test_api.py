def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200

def test_auth_required(client):
    res = client.post("/api/predict", json=[])
    assert res.status_code == 401
