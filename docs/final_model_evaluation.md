Final Model Evaluation – EcoPackAI
Project

EcoPackAI – AI-Powered Sustainable Packaging Recommendation System

Module

Model Evaluation, Explainability & Deployment Readiness

🎯 Objective

This document presents the final evaluation of all trained machine learning models used in EcoPackAI, covering:

Cost prediction

CO₂ emission prediction

Model comparison

Final model selection for deployment

The goal is to ensure models are accurate, stable, generalizable, and production-ready.

🧠 Models Evaluated
Model	Target Variable
Linear Regression	Cost per Unit
Decision Tree Regressor	Cost & CO₂
Random Forest Regressor	Cost per Unit
XGBoost Regressor	CO₂ Emission per Unit
📈 Evaluation Metrics Used

All models were evaluated using:

MAE (Mean Absolute Error) – average prediction error

RMSE (Root Mean Squared Error) – penalizes large errors

R² Score – variance explained by the model

Cross-Validation MAE – generalization stability

📊 Baseline Model Performance
Cost Prediction (Baseline)
Model	MAE	RMSE	R²	CV MAE
Linear Regression	~0.36	~0.71	~0.99	~0.36
Decision Tree	~0.003	~0.031	~0.999	~0.0029
CO₂ Prediction (Baseline)
Model	MAE	RMSE	R²	CV MAE
Linear Regression	~0.041	~0.059	~0.99	~0.041
Decision Tree	~0.0056	~0.017	~0.999	~0.0055
🌲 Advanced Model Performance
🔹 Random Forest – Cost Prediction
Metric	Value
MAE	0.0029
RMSE	0.0287
R²	0.99998
CV MAE	0.0028

Observation:

Strong improvement over Linear Regression

Very low error and excellent generalization

Selected as final cost prediction model

🔹 XGBoost – CO₂ Prediction
Metric	Value
MAE	0.00498
RMSE	0.01281
R²	0.99968

Observation:

Outperforms baseline and Decision Tree

Handles non-linear sustainability relationships well

Selected as final CO₂ prediction model

🏆 Final Model Selection
Task	Selected Model
Cost Prediction	Random Forest Regressor
CO₂ Prediction	XGBoost Regressor
🔍 Generalization & Stability

Models evaluated on hold-out test data

Cross-validation confirms low variance

No signs of overfitting despite high accuracy

Performance consistent across large integrated dataset

📦 Deployment Readiness

✔ Models serialized using joblib
✔ Preprocessing pipelines reused consistently
✔ Feature schemas fixed
✔ Metrics documented
✔ Explainability completed

📂 Final Artifacts
Artifact	Path
Cost Model	ml/models/rf_cost.joblib
CO₂ Model	ml/models/xgb_co2.joblib
Cost Metrics	ml/metrics/rf_cost_metrics.csv
CO₂ Metrics	ml/metrics/co2_metrics.csv
Explainability	docs/model_explainability.md
✅ Validation Checklist
Check	Status
Models evaluated on test data	✅
Metrics reviewed and documented	✅
Best models selected	✅
Deployment-ready artifacts	✅
🧾 Conclusion

EcoPackAI’s final models achieve high predictive accuracy, strong generalization, and explainable behavior, making them suitable for real-world sustainable packaging recommendation workflows.