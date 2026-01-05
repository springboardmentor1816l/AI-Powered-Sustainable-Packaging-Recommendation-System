# EcoPackAI – API Documentation

## Base URL
http://127.0.0.1:5000

yaml
Copy code

---

## 1️⃣ Health Check Endpoint

### Endpoint
GET /health

csharp
Copy code

### Description
Checks whether the EcoPackAI API service is running.

### Response (200 OK)
```json
{
  "status": "ok",
  "service": "EcoPackAI API",
  "message": "Service is running"
}

2️⃣ Prediction Endpoint
Endpoint
POST /predict

Description

Returns predicted cost and CO₂ emission for given product–material inputs.

Input Format (JSON)
[
  {
    "product_weight": 1.5,
    "fragility_index": 3,
    "shipping_type": "Air",
    "category": "Electronics",
    "material_type": "Cardboard",
    "strength_mpa": 6,
    "weight_capacity": 5,
    "recyclability_percent": 85,
    "biodegradability_percent": 90
  }
]

Response Format (200 OK)
{
  "predictions": [
    {
      "predicted_cost": 0.40,
      "predicted_co2": 0.50
    }
  ]
}

Error Handling

400: Invalid or missing input

500: Internal server error

Notes

Models used: Random Forest (Cost), XGBoost (CO₂)

API designed for extension into production systems