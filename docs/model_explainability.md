## Model Explainability

### Method Used
Permutation Importance was used to explain the final models.

This method measures the decrease in model performance when a single
feature’s values are randomly shuffled, making it model-agnostic and
robust.

### Models Explained
- Cost prediction: Random Forest
- CO₂ prediction: XGBoost

### Key Observations
- Cost predictions are dominated by material-level attributes and usage indicators.
- CO₂ predictions rely heavily on carbon footprint proxies and recyclability metrics.
- No identifier or target leakage features appear among the top contributors.

### Artifacts
- rf_cost_feature_importance.csv / .png
- xgb_co2_feature_importance.csv / .png

Permutation importance was chosen over SHAP to ensure cross-platform
reproducibility on Windows systems.
