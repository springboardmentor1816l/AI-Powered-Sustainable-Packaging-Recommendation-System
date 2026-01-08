import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

@pytest.fixture
def client():
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_predict_without_api_key(client):
    response = client.get("/predict/bottle")
    assert response.status_code == 401


def test_predict_with_api_key(client):
    response = client.get(
        "/predict/bottle",
        headers={"x-api-key": "mysecretkey123"}
    )
    assert response.status_code == 200
    assert response.get_json()["product"] == "bottle"
