# Data Quality Rules

These rules ensure that the materials and products datasets are clean, consistent, and ready for ML pipelines.

---

## 1. Missing Value Rules
- No nulls allowed in:
  - material_id
  - cost_per_kg
  - co2_emission_score
  - biodegradability_percent
  - recyclability_percent
  - CII, CEI, MSS
- Products dataset:
  - product_id, product_weight, fragility_index must not be null
  - required_load, required_moisture, required_thermal must not be null

---

## 2. Value Range Rules
- cost_per_kg > 0  
- co2_emission_score ≥ 0  
- biodegradability_percent ≥ 0  
- recyclability_percent ≥ 0  
- strength_mpa ≥ 0  
- product_weight ≥ 0  
- fragility_index ≥ 0  
- required_load: 1–10  
- required_moisture: 1–10  
- required_thermal: 1–10  
- CII, CEI, MSS: 0–100

---

## 3. Categorical Rules
Allowed categories:
- Material types: Paper, Plastic, Metal, Bio-based, Cardboard
- Recyclability grades: A, B, C, D
- Product categories (one-hot encoded): must be 0 or 1 only
- Shipping types: Standard, Heavy only

---

## 4. Uniqueness & Integrity Rules
- material_id must be unique  
- product_id must be unique  
- No duplicate rows allowed  
- No negative weights or dimensions  

---

## 5. Normalization Checks
Ensure the following are normalized 0–1:
- strength_mpa  
- weight_capacity  
- biodegradability_percent  
- co2_emission_score  
- recyclability_percent  

---

## 6. Feature Engineering Rules
- CII, CEI, MSS must be in the range 0–100  
- No inf, -inf, or NaN allowed  

