# Material Ranking Module Documentation

## Overview
The Material Ranking Module is designed to generate a ranked list of materials for each product based on predictive cost, CO₂ emissions, material suitability, and sustainability metrics. It integrates model predictions with business constraints to provide actionable recommendations for material selection.

The output is a **ranked CSV file** highlighting the top N materials per product.

---

## Inputs

1. **Processed Feature Dataset**
   - Path: `data/processed/X_raw.csv`
   - Includes product and material features such as weight, fragility index, recyclability, material type, packaging type, and other engineered features.

2. **Predicted Values**
   - **Cost Predictions:** `data/predictions/cost_predictions.csv`  
     Columns: `product_id`, `Material ID`, `predicted_cost`
   - **CO₂ Emission Predictions:** `data/predictions/co2_predictions.csv`  
     Columns: `product_id`, `Material ID`, `predicted_co2`

3. **Configuration File**
   - Path: `config/ranking_weights.yaml`
   - Defines:
     - `weights`: weight of each criterion in composite ranking.
     - `constraints`: thresholds for filtering materials.
     - `top_n`: number of top-ranked materials to return per product.

---

## Ranking Criteria

Each material is evaluated based on four key dimensions:

1. **Cost Efficiency**
   - Predicted cost per unit (lower is better)
   - Normalized using MinMaxScaler

2. **Environmental Impact**
   - Predicted CO₂ emission per unit (lower is better)
   - Normalized using MinMaxScaler

3. **Material Suitability**
   - A custom engineered score representing suitability of material for the product (higher is better)
   - Normalized using MinMaxScaler

4. **Sustainability Compliance**
   - Recyclability or other sustainability metrics (higher is better)
   - Normalized using MinMaxScaler

---

## Ranking Logic

1. **Normalization**
   All numeric metrics are normalized to the range `[0,1]` using `MinMaxScaler` to ensure comparability.

2. **Composite Ranking Score**
   The ranking score is computed as:
   ranking_score = (weights["cost"] * cost_norm) + (weights["co2"] * co2_norm) - (weights["suitability"] * suitability_norm) -(weights["sustainability"] * sustainability_norm) - Lower `ranking_score` indicates a better material choice.

3. **Constraint Filtering**
Before ranking, materials are filtered based on constraints defined in the YAML configuration:
- Minimum recyclability
- Minimum load handling score
- Minimum moisture resistance score
- Minimum thermal resistance score

Materials that do not meet these thresholds are excluded from ranking.

4. **Ranking**
- Materials are grouped by `product_id`.
- Ranked using **dense ranking** on the composite score.
- Only the **top N materials** are retained per product.

---

## Output

1. **File Path:** `outputs/material_rankings.csv`
2. **Columns:**
- `product_id`
- `Material ID`
- `predicted_cost`
- `predicted_co2`
- `Material Suitability Score`
- `Recyclability (%)`
- `ranking_score`
- `rank`
3. **Format:** CSV, sorted by `product_id` and `ranking_score`.

---
