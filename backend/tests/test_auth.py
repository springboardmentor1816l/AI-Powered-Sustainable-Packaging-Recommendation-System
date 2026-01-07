def test_predict_unauthorized(client):
    res = client.post("/api/predict", json={"product_weight_kg": 1.2})
    assert res.status_code == 401


def test_predict_authorized(client):
    res = client.post(
        "/api/predict",
        json={"product_weight_kg": 1.2},
        headers={"X-API-KEY": "ecopack-secret-key"}
    )
    assert res.status_code == 200
    assert res.json["status"] == "success"
