EcoPackAI – API Documentation

Overview
EcoPackAI exposes machine learning models through a REST API to predict
packaging cost impact and CO₂ emissions based on product and material attributes.
The API is designed for real-time inference and integration with recommendation systems.

Base URL
http://127.0.0.1:5000

--------------------------------------------------

Health Check Endpoint

Endpoint
GET /health

Description
Checks whether the API service is running and ready to accept requests.

Request
No request body required.

Response (200 OK)

{
  "status": "ok",
  "service": "EcoPackAI Model API"
}

Notes
- No authentication required
- No model inference is performed
- Used for monitoring and deployment readiness

--------------------------------------------------

Prediction Endpoint

Endpoint
POST /api/predict

Description
Accepts raw product and material inputs, internally adapts them to the
trained feature schema, applies preprocessing and machine learning models,
and returns predicted cost and CO₂ impact.

--------------------------------------------------

Request Body (JSON)

Required Fields

product_weight_kg
Type: float
Description: Weight of the product in kilograms

fragility_index
Type: float
Description: Fragility score (0–1 scale)

category
Type: string
Description: Product category (e.g., Food, Electronics, Pharmacy)

material_type
Type: string
Description: Packaging material type (e.g., Cardboard, Plastic)

recyclability_percent
Type: float
Description: Recyclability percentage of the material

co2_per_kg
Type: float
Description: Estimated CO₂ emission per kg of material

Example Request

{
  "product_weight_kg": 1.2,
  "fragility_index": 0.7,
  "category": "Food",
  "material_type": "Cardboard",
  "recyclability_percent": 80,
  "co2_per_kg": 1.1
}

--------------------------------------------------

Response Body (JSON)

Success Response (200 OK)

{
  "status": "success",
  "results": [
    {
      "predicted_cost": 0.07468401968401972,
      "predicted_co2": 0.38053223490715027
    }
  ]
}

Response Fields

predicted_cost
Description: Predicted cost impact per unit

predicted_co2
Description: Predicted CO₂ emissions per unit

status
Description: Request execution status

--------------------------------------------------

Error Responses

400 – Invalid Input

{
  "error": "Invalid JSON"
}

Occurs when request body is missing or malformed.

500 – Internal Server Error

{
  "status": "error",
  "message": "<error details>"
}

Occurs when preprocessing or model inference fails.

--------------------------------------------------

Implementation Notes

- Models are loaded once at application startup
- Raw inputs are adapted to the training feature schema using an input adapter
- Missing features are safely defaulted to zero
- Schema-aligned inference prevents feature mismatch errors
- Designed to integrate with downstream ranking logic

--------------------------------------------------

Status
Production-ready

Module
Model Serving & API Layer

Task Coverage
Flask Application Skeleton
Health Check Endpoint
Prediction Endpoint with Input Validation
