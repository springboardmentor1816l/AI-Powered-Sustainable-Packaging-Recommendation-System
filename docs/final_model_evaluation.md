\# Final Model Evaluation Report



\## Overview

This document summarizes the final evaluation results for the trained machine learning models used in the EcoPackAI system. The models predict cost impact and CO₂ emissions for packaging material recommendations.



---



\## Cost Prediction Model

\- Model Type: Random Forest Regressor

\- Evaluation Dataset: Hold-out test set



\### Metrics

\- MAE: 5.219119914747575e-05

\- RMSE: 0.00013753631288074711

\- R² Score: 0.9999987088799841



The model demonstrates strong generalization performance and captures key cost drivers such as material weight and product category.



---



\## CO₂ Emission Prediction Model

\- Model Type: XGBoost Regressor

\- Evaluation Dataset: Hold-out test set



\### Metrics

\- MAE: 0.00010333823276959358

\- RMSE:0.00037470220454244774

\- R² Score: 0.9999893409617114



The model generalizes well and aligns with domain expectations, with product weight and usage emerging as dominant predictors.



---



\## Model Selection Rationale

The selected models provide a balance between predictive accuracy, interpretability, and deployment readiness.

