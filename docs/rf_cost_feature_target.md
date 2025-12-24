# Random Forest Cost Prediction – Feature & Target Selection

## Objective
This document defines the input features and target variable used
for training the Random Forest regression model to predict packaging
cost per unit in EcoPackAI.

---

## Feature Dataset (X)

The following features are selected from the integrated and processed
dataset. These features describe both product and material attributes.

### Product Features
- product_weight
- fragility_index
- shipping_type
- category

### Material Features
- material_type
- strength_mpa
- weight_capacity
- recyclability_percent
- biodegradability_percent

---

## Target Variable (Y)

- cost_per_kg

### Target Characteristics
- Type: Continuous (Regression)
- Unit: Cost per kilogram (normalized)
- Source: Material dataset

---

## Leakage Prevention
- cost_per_kg is excluded from feature set
- No derived feature uses cost information
- Target is only used during model training and evaluation

---

## Conclusion
The selected features provide sufficient descriptive power for cost
prediction while ensuring no target leakage and maintaining model
generalization.
