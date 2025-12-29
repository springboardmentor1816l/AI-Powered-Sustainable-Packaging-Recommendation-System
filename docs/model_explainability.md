📄 Model Explainability – EcoPackAI
Project

EcoPackAI – AI-Powered Sustainable Packaging Recommendation System

Module

Model Evaluation, Explainability & Deployment Readiness

🎯 Objective

The goal of model explainability is to understand and justify why the trained machine learning models produce specific predictions, particularly for:

Cost per unit prediction

CO₂ emission prediction

This improves:

Trust and transparency

Debugging capability

Business and sustainability decision-making

Stakeholder confidence

🧠 Models Explained
Model	Target Variable
Random Forest Regressor	Cost per Unit
XGBoost Regressor	CO₂ Emission per Unit
🔍 Explainability Techniques Used
1️⃣ Feature Importance (Tree-Based Models)

Both Random Forest and XGBoost natively provide feature importance scores based on:

Reduction in impurity (Random Forest)

Gain and split contribution (XGBoost)

These scores indicate how strongly each feature contributes to the prediction.

2️⃣ Global Feature Importance (XGBoost)

For the CO₂ prediction model, feature importance values were extracted and saved as:

reports/feature_importance.csv


This file ranks features by their contribution to CO₂ emission prediction.

📊 Key Influential Features Identified
🔹 CO₂ Emission Prediction (XGBoost)

Top contributing features include:

Product Weight (kg)

Heavier products require stronger and often more carbon-intensive materials.

Packaging Type

Different materials (Cardboard, Plastic, Bio-based) have distinct emission profiles.

Recyclability Percentage

Higher recyclability lowers overall environmental impact.

Shipping Type

Transport mode influences packaging strength and material choice.

Supplier Sustainability Compliance (%)

Suppliers with higher compliance tend to use greener materials.

🔹 Cost Prediction (Random Forest)

Key drivers include:

Material Type / Packaging Type

Load Handling Score

Moisture & Thermal Resistance Scores

Supplier Sustainability Compliance

Product Fragility Index

These features align with real-world packaging cost drivers.