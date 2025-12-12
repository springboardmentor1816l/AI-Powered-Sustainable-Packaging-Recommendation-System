# Feature Transformation Plan – EcoPackAI

This document describes the transformation steps needed to calculate the
engineered feature values for ML pipelines.

---

## Step 1: Load Dataset
Input: /data/processed/cleaned_integrated_materials.csv

---

## Step 2: Normalize Numeric Fields (0–1)
- CO₂ emissions
- biodegradation time
- recyclability percent
- cost_per_kg
- durability_score
- moisture/thermal scores
- load handling score

Normalize using:  
(value - min) / (max - min)

---

## Step 3: Encode Categorical Values
- recyclability rating (A–D → 1 to 0.25)
- material type bonus
- category match (0–1)

---

## Step 4: Compute Features

### 4.1 CO₂ Impact Index
Apply formula defined in engineering document.

### 4.2 Cost Efficiency Index
Apply economic scoring formula.

### 4.3 Material Suitability Score
Apply suitability formula.

---

## Step 5: Save Engineered Dataset
Output:  
/data/processed/engineered_features.csv

