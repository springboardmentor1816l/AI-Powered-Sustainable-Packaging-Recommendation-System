import pytest
from app import create_app
from src.db.database import db
from src.db.models.prediction import Prediction

API_KEY = "ecopack-secret-key"
FULL_PAYLOAD = {
    "product_weight": 10,
    "material_type": "paper",
    "recyclability_score": 0.8,

    "product_weight_kg": 10,
    "category": "general",
    "fragility_index": 0.5,
    "shipping_type": "standard",

    "Material Type": "paper",
    "Packaging Type": "box",
    "Recyclability (%)": 80,
    "Recycled Content (%)": 50,
    "Reusability (%)": 40,
    "Waste Reduction Impact (%)": 30,
    "Supplier Sustainability Compliance (%)": 70,
    "Recyclability Category": "Medium",
    "Load Handling Score": 70,
    "Moisture Resistance Score": 60,
    "Thermal Resistance Score": 65,
    "Supplier Region": "Asia",
    "Biodegradation Time (days)": 180
}


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            yield client


# -------------------------
# Health Check Tests
# -------------------------
def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


# -------------------------
# Security Tests
# -------------------------
def test_predict_without_api_key(client):
    response = client.post("/predict", json={})
    assert response.status_code == 401


def test_predict_with_invalid_api_key(client):
    response = client.post(
        "/predict",
        headers={"X-API-Key": "wrong-key"},
        json={}
    )
    assert response.status_code == 403


# -------------------------
# Validation Tests
# -------------------------
def test_predict_missing_fields(client):
    response = client.post(
        "/predict",
        headers={"X-API-Key": API_KEY},
        json={"product_weight": 10}
    )
    assert response.status_code == 400


# -------------------------
# Successful Prediction Test
# -------------------------
def test_predict_success(client):
    FULL_PAYLOAD = {
        "product_weight": 10,
        "material_type": "paper",
        "recyclability_score": 0.8,

        "product_weight_kg": 10,
        "category": "general",
        "fragility_index": 0.5,
        "shipping_type": "standard",

        "Material Type": "paper",
        "Packaging Type": "box",
        "Recyclability (%)": 80,
        "Recycled Content (%)": 50,
        "Reusability (%)": 40,
        "Waste Reduction Impact (%)": 30,
        "Supplier Sustainability Compliance (%)": 70,
        "Recyclability Category": "Medium",
        "Load Handling Score": 70,
        "Moisture Resistance Score": 60,
        "Thermal Resistance Score": 65,
        "Supplier Region": "Asia",
        "Biodegradation Time (days)": 180
    }


    response = client.post(
        "/predict",
        headers={"X-API-Key": API_KEY},
        json=FULL_PAYLOAD
    )


    assert response.status_code == 200
    data = response.get_json()

    assert "prediction" in data
    assert "predicted_cost" in data["prediction"]
    assert "predicted_co2" in data["prediction"]


# -------------------------
# Database Persistence Test
# -------------------------
def test_prediction_saved_to_db(client):
    payload = {
        "product_weight": 20,
        "material_type": "plastic",
        "recyclability_score": 0.5
    }

    initial_count = Prediction.query.count()

    response = client.post(
        "/predict",
        headers={"X-API-Key": API_KEY},
        json=FULL_PAYLOAD
    )

    assert response.status_code == 200
    assert Prediction.query.count() == initial_count + 1
