import pytest
from api.app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()

def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}

def test_predict_without_api_key(client):
    response = client.post(
        "/predict",
        json={
            "category": "Electronics",
            "material_type": "Cardboard",
            "biodegradability_percent": 90
        }
    )

    assert response.status_code == 401
    assert "error" in response.json


def test_predict_with_api_key(client):
    response = client.post(
        "/predict",
        headers={
            "X-API-KEY": "ecopackai-secret"
        },
        json={
            "category": "Electronics",
            "material_type": "Cardboard",
            "biodegradability_percent": 90
        }
    )

    assert response.status_code == 200
    assert "predictions" in response.json

