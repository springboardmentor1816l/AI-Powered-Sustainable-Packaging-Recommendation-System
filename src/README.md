# Model Explainability & Inference - Quick Start

## Overview

This directory contains tools for model interpretation (explainability) and production inference.

## Modules

### 1. Explainability (`src/explainability/`)

Interpret and explain ML model predictions using SHAP and feature importance.

**Key Features**:
- SHAP value calculation
- Global feature importance
- Local prediction explanations
- Feature dependence analysis
- Automated report generation

**Quick Start**:
```bash
python scripts/generate_explainability.py
```

### 2. Inference (`src/inference/`)

Unified prediction interface for cost and CO₂ models.

**Key Features**:
- Single/batch predictions
- Confidence intervals
- Model validation
- CSV batch processing
- Metadata management

**Quick Start**:
```python
from src.inference.predictor import EcoPackPredictor

predictor = EcoPackPredictor()
result = predictor.predict_single(features_dict)
```

## Dependencies

```bash
pip install pandas numpy scikit-learn xgboost joblib shap matplotlib seabornpyyaml
```

## Documentation

- **Explainability**: `docs/model_explainability.md`
- **Evaluation**: `docs/final_model_evaluation.md`
- **Summary**: `docs/EXPLAINABILITY_PACKAGING_SUMMARY.md`

## Output Artifacts

- **Explainability**: `outputs/explainability/`
- **Predictions**: `outputs/predictions/`

## Status

✅ Production Ready  
📅 Last Updated: 2026-01-02  
👥 Team: EcoPackAI Development
