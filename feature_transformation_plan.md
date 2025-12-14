# Feature Transformation Plan

This document describes the complete step-by-step process for transforming cleaned material data into engineered features used by EcoPackAI. No code is included—only logic and workflow.

---

# 1. Overview
The goal of the feature transformation pipeline is to convert raw sustainability, cost, and performance attributes into three standardized indices:
- **CO₂ Impact Index (CII)**
- **Cost Efficiency Index (CEI)**
- **Material Suitability Score (MSS)**

These indices become core inputs for recommendations, scoring dashboards, and future ML models.

---

# 2. Input Columns Required
The transformation depends on the following fields from the cleaned dataset:

### Environmental Inputs
- `Carbon Footprint (kg CO2/unit)`
- `Biodegradation Time (days)`
- `Recyclability Category`

### Cost Inputs
- `Cost per Unit (USD)`
- `Total Material Weight (tons)`
- `Durability Rating`

### Suitability Inputs
- `Load Handling Score`
- `Moisture Resistance Score`
- `Thermal Resistance Score`
- `Suitable Product Categories`

---

# 3. Preprocessing Steps for Transformation
Before calculating indices, the following preprocessing rules are applied:

### 3.1 Convert Units
- `Total Material Weight (tons)` → converted to kilograms for consistency.

### 3.2 Handle Recyclability
`Recyclability Category` is mapped to numerical values:
- A → 1.00
- B → 0.75
- C → 0.50
- D → 0.25

### 3.3 Normalize Selected Columns
Normalization rule:
```
normalized_value = (value - min) / (max - min)
```
Used for:
- Carbon Footprint
- Load Handling Score

### 3.4 Scale Values to 0–1
For scores already on 0–10 scale:
```
scaled_value = score / 10
```
Used for:
- Moisture Resistance Score
- Thermal Resistance Score
- Durability Rating

---

# 4. Transformation Steps for Each Engineered Feature

## 4.1 CO₂ Impact Index (CII)

### Step-by-Step Logic
1. Normalize `Carbon Footprint (kg CO2/unit)`.
2. Normalize `Biodegradation Time (days)` and convert it into an eco-friendly score.
3. Convert `Recyclability Category` into numeric score.
4. Compute the final weighted index:
```
CII = 0.40 * (1 - normalized carbon footprint)
    + 0.30 * biodegradation score
    + 0.30 * recyclability score
```
5. Output is scaled between 0 and 1.

---

## 4.2 Cost Efficiency Index (CEI)

### Step-by-Step Logic
1. Normalize `Cost per Unit (USD)`.
2. Convert `Total Material Weight (tons)` → kg.
3. Scale `Durability Rating` to 0–1.
4. Convert `Recyclability Category` to numeric score.
5. Compute final weighted index:
```
CEI = 0.50 * normalized cost
    + 0.20 * recyclability score
    + 0.30 * durability score
```
6. Output is scaled between 0 and 1.

---

## 4.3 Material Suitability Score (MSS)

### Step-by-Step Logic
1. Normalize `Load Handling Score`.
2. Scale:
   - `Moisture Resistance Score` → 0–1
   - `Thermal Resistance Score` → 0–1
   - `Durability Rating` → 0–1
3. Parse `Suitable Product Categories`.
4. Count number of categories and calculate:
```
category_bonus = min(number_of_categories * 0.02, 0.10)
```
5. Compute final weighted MSS:
```
MSS = 0.25 * load_score
    + 0.25 * moisture_score
    + 0.20 * thermal_score
    + 0.20 * durability_score
    + 0.10 * category_bonus
```
6. Output is scaled between 0 and 1.

---

# 5. Final Output Columns
Each record in the dataset receives three new engineered features:
- `CII` — CO₂ Impact Index
- `CEI` — Cost Efficiency Index
- `MSS` — Material Suitability Score

These become standardized inputs for downstream analytics, dashboards, and ML pipelines.

---

# 6. End-to-End Flow Summary
1. Read cleaned dataset.
2. Convert units and map recyclability.
3. Normalize and scale required attributes.
4. Generate CII, CEI, MSS using defined formulas.
5. Append the engineered features to the dataset.
6. Save or export the updated dataset for further use.

---

This completes the full transformation logic for EcoPackAI’s feature engineering pipeline.

