# Target–Feature Mapping & ML Problem Framing – EcoPackAI

## Overview
This document maps target variables to their corresponding input
features and defines the machine learning problem formulation
used in EcoPackAI.

---

## ML Problem Type

### Primary Model
- Problem Type: Multi-class Classification
- Objective: Predict the most suitable sustainable packaging material
- Output: recommended_material

---

### Secondary Models (Optional)
- Regression Model
  - Target: sustainability_score
  - Purpose: Ranking and explainability

- Classification Model
  - Target: cost_efficiency_category
  - Purpose: Budget-aware recommendations

---

## Target–Feature Mapping

### 1. Primary Target: recommended_material

**Model Type:** Multi-class Classification

**Input Features:**
- strength_mpa
- weight_capacity
- moisture_resistance_score
- thermal_resistance_score
- biodegradability_percent
- recyclability_percent
- co2_emission_score
- cost_per_kg
- material_type (one-hot encoded)
- indusrty_use_case (one-hot encoded)
- CO2_Impact_Index
- Cost_Efficiency_Index
- Material_Suitability_Score

**Justification:**
- Combines physical, environmental, cost, and suitability factors
- Enables context-aware material recommendation

---

### 2. Secondary Target: sustainability_score

**Model Type:** Regression

**Input Features:**
- co2_emission_score
- biodegradability_percent
- recyclability_percent
- CO2_Impact_Index

**Justification:**
- Aggregates sustainability indicators into a single interpretable score

---

### 3. Tertiary Target: cost_efficiency_category

**Model Type:** Classification

**Input Features:**
- cost_per_kg
- weight_capacity
- recyclability_percent
- Cost_Efficiency_Index

**Justification:**
- Enables cost-based grouping for business decisions

---

## Feature–Target Dependency Summary

| Target Variable | Model Type | Feature Groups Used |
|-----------------|-----------|---------------------|
| recommended_material | Classification | Material, Sustainability, Cost, Engineered |
| sustainability_score | Regression | Environmental, Engineered |
| cost_efficiency_category | Classification | Cost, Performance |

---

## Conclusion
This target–feature mapping ensures clear separation of objectives,
supports modular ML development, and allows EcoPackAI to scale with
multiple predictive models while maintaining interpretability.
