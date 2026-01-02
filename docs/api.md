# EcoPackAI API Documentation

## Overview

The EcoPackAI API provides machine learning-powered predictions for packaging material cost and CO₂ emissions. The API supports single predictions, batch processing, and model information retrieval.

**Base URL**: `http://localhost:5000` (Development)  
**API Version**: v1  
**Authentication**: None (add authentication in production)

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Health Endpoints](#health-endpoints)
3. [Prediction Endpoints](#prediction-endpoints)
4. [Request/Response Format](#requestresponse-format)
5. [Error Handling](#error-handling)
6. [Usage Examples](#usage-examples)

---

## Quick Start

### Starting the API

```bash
# Install dependencies
pip install flask flask-cors pandas numpy scikit-learn xgboost joblib psutil

# Run the API
python app.py
```

The API will start on `http://localhost:5000`

### Test Health Check

```bash
curl http://localhost:5000/health
```

### Make a Prediction

```bash
curl -X POST http://localhost:5000/api/v1/predict/all \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

---

## Health Endpoints

### 1. Basic Health Check

**Endpoint**: `GET /health`  
**Purpose**: Verify service is running  
**Response Time**: < 5ms

```bash
curl http://localhost:5000/health
```

**Response (200 OK)**:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-02T11:40:00",
  "service": "EcoPackAI API",
  "version": "1.0.0"
}
```

### 2. Readiness Check

**Endpoint**: `GET /health/ready`  
**Purpose**: Verify models are loaded and service is ready

```bash
curl http://localhost:5000/health/ready
```

**Response (200 OK)**:
```json
{
  "status": "ready",
  "timestamp": "2026-01-02T11:40:00",
  "models": {
    "cost_model": "loaded",
    "co2_model": "loaded"
  }
}
```

**Response (503 Service Unavailable)** - Not ready:
```json
{
  "status": "not_ready",
  "timestamp": "2026-01-02T11:40:00",
  "message": "Models not fully loaded"
}
```

### 3. Liveness Check

**Endpoint**: `GET /health/live`  
**Purpose**: Kubernetes liveness probe

```bash
curl http://localhost:5000/health/live
```

### 4. Detailed Health

**Endpoint**: `GET /health/detailed`  
**Purpose**: Comprehensive system status

```bash
curl http://localhost:5000/health/detailed
```

**Response includes**:
- Service information
- System resources (CPU, memory, disk)
- Model loading status
- Python version and platform

---

## Prediction Endpoints

### 1. Predict Cost

**Endpoint**: `POST /api/v1/predict/cost`  
**Purpose**: Predict packaging material cost per unit

**Request**:
```bash
curl -X POST http://localhost:5000/api/v1/predict/cost \
  -H "Content-Type: application/json" \
  -d '{
    "recyclability_percent": 95.0,
    "recycled_content_percent": 70.0,
    "reusability_percent": 50.0,
    "biodegradation_time_days": 120,
    "end_of_life_disposal_percent": 95.0,
    "carbon_footprint_kg_co2_unit": 1.8,
    "waste_reduction_impact_percent": 80.0,
    "sustainability_target_progress_percent": 85.0,
    "load_handling_score": 8.0,
    "moisture_resistance_score": 7.0,
    "thermal_resistance_score": 7.0,
    "annual_usage_units": 15000,
    "total_material_weight_tons": 7.5,
    "supplier_sustainability_compliance_percent": 90.0,
    "co2_impact_index": 0.25,
    "cost_efficiency_index": 0.75,
    "material_suitability_score": 70.0,
    "overall_sustainability_score": 0.85
  }'
```

**Response (200 OK)**:
```json
{
  "status": "success",
  "timestamp": "2026-01-02T11:40:00",
  "prediction_type": "cost",
  "results": {
    "predicted_cost": 12.45,
    "cost_confidence": 0.85
  }
}
```

### 2. Predict CO₂

**Endpoint**: `POST /api/v1/predict/co2`  
**Purpose**: Predict CO₂ emissions per kg

**Request**:
```bash
curl -X POST http://localhost:5000/api/v1/predict/co2 \
  -H "Content-Type: application/json" \
  -d '{...}'  # Same features as cost prediction
```

**Response (200 OK)**:
```json
{
  "status": "success",
  "timestamp": "2026-01-02T11:40:00",
  "prediction_type": "co2",
  "results": {
    "predicted_co2": 1.234
  }
}
```

### 3. Predict Both (Cost & CO₂)

**Endpoint**: `POST /api/v1/predict/all`  
**Purpose**: Predict both cost and CO₂ in single call

**Request**:
```bash
curl -X POST http://localhost:5000/api/v1/predict/all \
  -H "Content-Type: application/json" \
  -d '{...}'  # Same features
```

**Response (200 OK)**:
```json
{
  "status": "success",
  "timestamp": "2026-01-02T11:40:00",
  "prediction_type": "all",
  "results": {
    "predicted_cost": 12.45,
    "cost_confidence": 0.85,
    "predicted_co2": 1.234
  },
  "metadata": {
    "cost_model": "Random Forest",
    "co2_model": "XGBoost",
    "cost_r2": 0.997,
    "co2_r2": 0.994
  }
}
```

### 4. Batch Prediction

**Endpoint**: `POST /api/v1/predict/batch`  
**Purpose**: Predict for multiple materials at once

**Request**:
```bash
curl -X POST http://localhost:5000/api/v1/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "materials": [
      {
        "id": "material_1",
        "recyclability_percent": 95.0,
        ...
      },
      {
        "id": "material_2",
        "recyclability_percent": 80.0,
        ...
      }
    ]
  }'
```

**Response (200 OK)**:
```json
{
  "status": "success",
  "timestamp": "2026-01-02T11:40:00",
  "prediction_type": "batch",
  "count": 2,
  "results": [
    {
      "id": "material_1",
      "predicted_cost": 12.45,
      "cost_confidence": 0.85,
      "predicted_co2": 1.234
    },
    {
      "id": "material_2",
      "predicted_cost": 15.20,
      "cost_confidence": 0.78,
      "predicted_co2": 2.456
    }
  ]
}
```

### 5. Model Information

**Endpoint**: `GET /api/v1/models/info`  
**Purpose**: Get loaded model information

```bash
curl http://localhost:5000/api/v1/models/info
```

**Response (200 OK)**:
```json
{
  "status": "success",
  "timestamp": "2026-01-02T11:40:00",
  "models": {
    "cost_model": {
      "loaded": true,
      "path": "ml/models/rf_cost.joblib",
      "type": "RandomForestRegressor"
    },
    "co2_model": {
      "loaded": true,
      "path": "ml/models/xgb_co2.joblib",
      "type": "XGBRegressor"
    },
    "metadata": {
      "version": "1.0.0",
      "project": "EcoPackAI"
    }
  }
}
```

### 6. API Documentation

**Endpoint**: `GET /api/v1/docs`  
**Purpose**: Get API schema and examples

```bash
curl http://localhost:5000/api/v1/docs
```

---

## Request/Response Format

### Required Features (18 fields)

All prediction endpoints require the following features:

| Feature | Type | Range | Description |
|---------|------|-------|-------------|
| `recyclability_percent` | float | 0-100 | Material recyclability % |
| `recycled_content_percent` | float | 0-100 | Recycled content % |
| `reusability_percent` | float | 0-100 | Material reusability % |
| `biodegradation_time_days` | float | 0-3650 | Biodegradation time in days |
| `end_of_life_disposal_percent` | float | 0-100 | Disposal efficiency % |
| `carbon_footprint_kg_co2_unit` | float | 0-50 | Carbon footprint per unit |
| `waste_reduction_impact_percent` | float | 0-100 | Waste reduction impact % |
| `sustainability_target_progress_percent` | float | 0-100 | Sustainability progress % |
| `load_handling_score` | float | 1-10 | Load handling capability |
| `moisture_resistance_score` | float | 1-10 | Moisture resistance |
| `thermal_resistance_score` | float | 1-10 | Thermal resistance |
| `annual_usage_units` | float | 0+ | Annual usage volume |
| `total_material_weight_tons` | float | 0+ | Total material weight |
| `supplier_sustainability_compliance_percent` | float | 0-100 | Supplier compliance % |
| `co2_impact_index` | float | 0-1 | Engineered CO₂ index |
| `cost_efficiency_index` | float | 0-1 | Cost efficiency index |
| `material_suitability_score` | float | 0-100 | Material suitability |
| `overall_sustainability_score` | float | 0-1 | Overall sustainability |

### Response Fields

**Success Response**:
- `status`: "success"
- `timestamp`: ISO 8601 timestamp
- `prediction_type`: "cost", "co2", "all", or "batch"
- `results`: Prediction results object
- `metadata`: Optional metadata

**Results Object** (for `/predict/all`):
- `predicted_cost`: Predicted cost in USD
- `cost_confidence`: Confidence interval (±)
- `predicted_co2`: Predicted CO₂ in kg per kg

---

## Error Handling

### Error Response Format

```json
{
  "status": "error",
  "timestamp": "2026-01-02T11:40:00",
  "error": "Error Type",
  "message": "Detailed error message"
}
```

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Prediction successful |
| 400 | Bad Request | Invalid input data |
| 404 | Not Found | Endpoint doesn't exist |
| 500 | Server Error | Model prediction failed |
| 503 | Unavailable | Service not ready |

### Common Errors

#### 1. Missing Required Features

**Request**: Missing `recyclability_percent`

**Response (400)**:
```json
{
  "status": "error",
  "timestamp": "2026-01-02T11:40:00",
  "error": "Validation Error",
  "message": "Missing required features: recyclability_percent, recycled_content_percent..."
}
```

#### 2. Invalid Feature Values

**Request**: `load_handling_score = 15` (out of range 1-10)

**Response (400)**:
```json
{
  "status": "error",
  "timestamp": "2026-01-02T11:40:00",
  "error": "Validation Error",
  "message": "Invalid feature values: load_handling_score (15 not in range [1, 10])"
}
```

#### 3. Non-Numeric Values

**Request**: `recyclability_percent = "high"`

**Response (400)**:
```json
{
  "status": "error",
  "timestamp": "2026-01-02T11:40:00",
  "error": "Validation Error",
  "message": "Invalid feature values: recyclability_percent (not numeric)"
}
```

---

## Usage Examples

### Python Client

```python
import requests

# API endpoint
url = "http://localhost:5000/api/v1/predict/all"

# Material features
features = {
    "recyclability_percent": 95.0,
    "recycled_content_percent": 70.0,
    "reusability_percent": 50.0,
    "biodegradation_time_days": 120,
    "end_of_life_disposal_percent": 95.0,
    "carbon_footprint_kg_co2_unit": 1.8,
    "waste_reduction_impact_percent": 80.0,
    "sustainability_target_progress_percent": 85.0,
    "load_handling_score": 8.0,
    "moisture_resistance_score": 7.0,
    "thermal_resistance_score": 7.0,
    "annual_usage_units": 15000,
    "total_material_weight_tons": 7.5,
    "supplier_sustainability_compliance_percent": 90.0,
    "co2_impact_index": 0.25,
    "cost_efficiency_index": 0.75,
    "material_suitability_score": 70.0,
    "overall_sustainability_score": 0.85
}

# Make request
response = requests.post(url, json=features)

# Parse response
if response.status_code == 200:
    data = response.json()
    print(f"Predicted Cost: ${data['results']['predicted_cost']:.2f}")
    print(f"Predicted CO₂: {data['results']['predicted_co2']:.4f} kg")
else:
    print(f"Error: {response.json()['message']}")
```

### JavaScript Client

```javascript
const url = 'http://localhost:5000/api/v1/predict/all';

const features = {
  recyclability_percent: 95.0,
  recycled_content_percent: 70.0,
  // ... other features
};

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(features)
})
.then(response => response.json())
.then(data => {
  console.log('Predicted Cost:', data.results.predicted_cost);
  console.log('Predicted CO₂:', data.results.predicted_co2);
})
.catch(error => console.error('Error:', error));
```

### Batch Processing Example

```python
import pandas as pd
import requests

# Load materials from CSV
materials_df = pd.read_csv('materials.csv')

# Prepare batch request
batch_request = {
    "materials": materials_df.to_dict('records')
}

# Make batch prediction
response = requests.post(
    "http://localhost:5000/api/v1/predict/batch",
    json=batch_request
)

# Convert to DataFrame
predictions_df = pd.DataFrame(response.json()['results'])

#Save predictions
predictions_df.to_csv('predictions.csv', index=False)
```

---

## Deployment

### Production Considerations

1. **WSGI Server**: Use `gunicorn` instead of Flask dev server
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Authentication**: Add API key or OAuth authentication

3. **Rate Limiting**: Implement rate limiting for API endpoints

4. **HTTPS**: Use SSL/TLS certificates

5. **Monitoring**: Set up logging and monitoring

6. **Caching**: Cache frequent predictions

### Docker Deployment

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

---

## Support

For API support:
- **Documentation**: This file
- **Schema**: `docs/api_schema.json`
- **Team**: EcoPackAI Development Team

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-02  
**Status**: ✅ Production Ready
