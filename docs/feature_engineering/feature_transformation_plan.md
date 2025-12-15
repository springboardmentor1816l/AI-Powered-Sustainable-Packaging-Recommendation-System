# Feature Transformation Plan
This document describes the step-by-step process used to transform raw dataset columns into the engineered features for EcoPackAI.

---

## Step 1 — Load & Normalize Inputs
- Read materials dataset.
- Ensure all numeric columns are within 0–1 or correctly scaled.
- Check for missing or invalid values.

---

## Step 2 — Compute CII (CO2 Impact Index)
1. Start with normalized CO₂ emission score.
2. Add biodegradability contribution.
3. Add recyclability contribution.
4. Combine using predefined weights.
5. Scale final value to 0–100.

---

## Step 3 — Compute CEI (Cost Efficiency Index)
1. Normalize cost_per_kg.
2. Apply an inverse cost contribution (lower cost → higher score).
3. Add a strength contribution for durability.
4. Scale to 0–100.

---

## Step 4 — Compute MSS (Material Suitability Score)
1. Evaluate material strength (0–1).
2. Include weight capacity performance.
3. Add recyclability contribution.
4. Combine these into an overall suitability score.
5. Scale to 0–100.

---

## Step 5 — Add Required Columns to Products Dataset
- required_load → based on product_weight scaling
- required_moisture → assigned based on product category
- required_thermal → based on category + shipping type

---

## Step 6 — Validate All Feature Values
- No missing values  
- No negative values  
- All values are within ranges  
- All encoded categories are correct  

---

## Step 7 — Export Updated Datasets
- materials_updated.csv
- products_updated.csv

These datasets are now ready for Week 9 & 10 modeling pipelines and recommendation scoring.

