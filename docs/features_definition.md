# Feature Definition – EcoPackAI

## Overview
This document defines the input features used by the EcoPackAI
machine learning model to recommend sustainable packaging materials.

Features are selected from cleaned, engineered, and model-ready datasets
after validation and preprocessing.

---

## Feature Categories

### 1. Material Properties (Numeric)
These features describe physical and environmental characteristics
of packaging materials.

- strength_mpa
- weight_capacity
- moisture_resistance_score
- thermal_resistance_score
- biodegradability_percent
- recyclability_percent
- co2_emission_score
- cost_per_kg

Purpose:
- Assess durability, safety, sustainability, and cost efficiency.

---

### 2. Material Type Features (Categorical → Encoded)
These features identify the base material used.

- material_type (Paper, Plastic, Metal, Bio-based)

Encoding:
- One-Hot Encoding applied in model-ready dataset.

Purpose:
- Enable model to differentiate sustainability profiles by material.

---

### 3. Industry / Use-Case Features (Categorical → Encoded)
These features represent intended application or industry.

- indusrty_use_case (e.g., E-commerce, Food & Beverage, Electronics)

Encoding:
- One-Hot Encoding applied.

Purpose:
- Match material suitability to product category and handling needs.

---

### 4. Engineered Sustainability Features
These features are derived from raw attributes to improve model learning.

- CO2_Impact_Index
- Cost_Efficiency_Index
- Material_Suitability_Score

Purpose:
- Provide high-level, interpretable signals for recommendations.
- Improve ranking and explainability.

---

## Excluded Columns
The following columns are excluded from model training:

- material_id (identifier only)
- free-text notes
- supplier comments
- any metadata not impacting material selection

---

## Feature Scaling
- Numeric features are scaled using MinMaxScaler (0–1).
- Encoded categorical features remain binary (0 or 1).

---

## Final Feature Set
The final model input consists of:
- Scaled numeric features
- One-hot encoded categorical features
- Engineered sustainability features

---

## Conclusion
The selected features ensure that EcoPackAI models are trained on
relevant, high-quality inputs that balance sustainability, cost,
and material performance.
