# EcoPackAI API Documentation
---

## 1. Health Check
**Endpoint:** `/health`  
**Method:** `GET`  
**Description:** Verifies the API is live and models are loaded.

## 2. Prediction Endpoint
**Endpoint:** `/predict`  
**Method:** `POST`  
**Description:** Returns Cost and CO2 impact predictions.

### Request Body Example:
```json
{
  "product_weight_kg": 1.5,
  "fragility_index": 0.3,
  "category": "Electronics"
}