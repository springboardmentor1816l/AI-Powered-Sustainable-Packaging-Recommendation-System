# EcoPackAI Model API

## Health Check
**GET /health**

Returns service status.

---

## Prediction Endpoint
**POST /api/predict**

### Request Body
See `api_schema.json`

### Response
```json
{
  "predictions": {
    "predicted_cost_per_unit": 0.42,
    "predicted_co2_emission": 0.018
  },
  "model_metadata": {
    "cost_model": "RandomForest v1",
    "co2_model": "XGBoost v1"
  }
}
