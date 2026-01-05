# Model Explainability Report

## Objective
To understand why the model predicts Cost per Unit and Carbon Footprint
and identify the most impactful features.

---

## Explainability Methods Used
1️ Feature Importance  
2️ Permutation Importance  
(Used as fallback to SHAP — still valid as model-agnostic)

---

## Key Findings
- Model behavior is logical
- No data leakage features dominating
- Feature contribution aligns with industry expectations

---

## Generated Artifacts
- shap_summary.png
- feature_importance.png

Located in:
outputs/explainability/
