## EcoPackAI API

### Health Check
GET /health

Response:
{
  "status": "UP",
  "service": "EcoPackAI API"
}

---

### Prediction Endpoint
POST /api/predict

Request JSON:
{
  "product_weight_kg": 1.2,
  "fragility_index": 3,
  "shipping_type": "Air",
  "Material Type": "Paper",
  "Recyclability Category": "A",
  "Load Handling Score": 7
}

Response:
{
  "predicted_cost": 2.45,
  "predicted_co2": 0.81
}
