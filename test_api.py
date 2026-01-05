import pytest
from app import create_app

API_KEY = "ecopackai-secret-key"


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_predict_without_api_key(client):
    response = client.post(
        "/api/predict",
        json={"product_id": 1}
    )
    assert response.status_code == 401  # masked auth


def test_predict_with_invalid_payload(client):
    response = client.post(
        "/api/predict",
        headers={"X_API_KEY": API_KEY},
        json={}
    )
    assert response.status_code == 400  # masked validation


def test_predict_success(client):
    response = client.post(
        "/api/predict",
        headers={"X_API_KEY": API_KEY},
        json={
            "product_id": 1,
            "material_id": "MAT_0001"
        }
    )
    assert response.status_code == 200

    data = response.get_json()
    assert data["status"] == "success"
    assert "results" in data
    assert "predicted_cost" in data["results"][0]
    assert "predicted_co2" in data["results"][0]
