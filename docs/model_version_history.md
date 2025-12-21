# Model Version History
Project: EcoPackAI – AI-Powered Sustainable Packaging Recommendation System

## Purpose
This document tracks all trained model versions, their configurations, and performance.
It ensures reproducibility, traceability, and safe model evolution.

---

## Versioning Rules
- Version format: v1, v2, v3, ...
- New version created when:
  - Dataset changes
  - Feature set changes
  - Model hyperparameters change
- Older versions are retained for comparison and rollback.

---

## Model Versions

### v1 — Baseline Models
**Date:** 2025-12-21  
**Models:**
- Linear Regression (Cost Prediction)
- Linear Regression (CO₂ Prediction)
- Decision Tree Regressor (Cost Prediction)
- Decision Tree Regressor (CO₂ Prediction)

**Dataset:** Integrated Product–Material Dataset v1  
**Features:** Engineered numeric + encoded categorical features  
**Evaluation:** MAE, RMSE, R², Cross-validation MAE  

**Notes:**
Baseline models trained for performance benchmarking.
