# Feature Transformation Plan — EcoPackAI

## Input Dataset
- cleaned_integrated_materials.csv

## Output Dataset
- materials_feature_engineered.csv

---

## Transformation Steps

### Step 1: Normalize Base Numeric Features
- Carbon Footprint
- Cost per kg
- Biodegradation Time
- Weight Capacity

Purpose: Ensure comparability before aggregation.

---

### Step 2: Map Recyclability Category
Applied decimal mapping:
A → 1.0, B → 0.75, C → 0.5, D → 0.25

---

### Step 3: Compute CO₂ Impact Index
Weighted aggregation of normalized inputs.
Scaled to 0–100.

---

### Step 4: Compute Cost Efficiency Index
Weighted combination of cost, strength, and recyclability.
Scaled to 0–100.

---

### Step 5: Compute Material Suitability Score
- Evaluated per (material × product category)
- Based on compatibility rules
- Scaled to 0–100

---

### Step 6: Compute Final Recommendation Score
Weighted average of CII, CEI, and MSS.

---

## Validation Checks
- No missing values introduced
- All engineered features within 0–100
- Traceable to original columns
