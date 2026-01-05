import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_unauthorized(client):
    res = client.post("/predict", json={})
    assert res.status_code == 401

