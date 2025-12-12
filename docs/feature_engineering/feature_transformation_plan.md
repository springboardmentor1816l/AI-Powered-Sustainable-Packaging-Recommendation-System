# Feature Engineering Document – EcoPackAI

This document defines the three major engineered features used in
EcoPackAI to support sustainability scoring and ML model training.

---

## 1. CO₂ Impact Index (CII)

### Objective:
To measure the environmental impact of a packaging material using a
normalized sustainability score (0–100).

### Inputs:
- CO₂ emissions per kg
- Biodegradation time (days)
- Recyclability rating (A–D)
- Material type

### Normalization:
All numeric features are scaled 0–1.

### Recyclability Mapping:
A → 1.0  
B → 0.75  
C → 0.5  
D → 0.25  

### Material Bonus:
Bio-based → +0.10  
Paper → +0.05  
Plastic → 0  
Metal → -0.05  

### Formula Structure:
CII = 100 * (
    0.4 * (1 - CO2_norm) +
    0.2 * (1 - biodeg_norm) +
    0.3 * recyclability_score +
    0.1 * material_bonus
)

---

## 2. Cost Efficiency Index (CEI)

### Objective:
To determine the cost-performance of packaging materials.

### Inputs:
- cost_per_kg
- weight_required_for_packaging
- recyclability_percent
- durability_score

### Scoring:
Lower cost → higher score  
Higher durability → higher score  
Higher recyclability → higher score  
Lower weight used → higher score  

### Formula Structure:
CEI = 100 * (
    0.4 * (1 - cost_norm) +
    0.3 * durability_norm +
    0.2 * recyclability_norm +
    0.1 * (1 - weight_required_norm)
)

---

## 3. Material Suitability Score (MSS)

### Objective:
To measure how suitable a material is for a given product category.

### Inputs:
- load_handling_score
- moisture_resistance_score
- thermal_resistance_score
- product_category_requirements
- fragility_level

### Category Match Logic:
- If material fails a mandatory requirement → strong penalty  
- If material exceeds category requirements → bonus  

### Formula Structure:
MSS = 100 * (
    0.3 * load_norm +
    0.25 * moisture_norm +
    0.25 * thermal_norm +
    0.2 * category_match
)

---

## Output Feature Columns:
- CO2_Impact_Index
- Cost_Efficiency_Index
- Material_Suitability_Score

