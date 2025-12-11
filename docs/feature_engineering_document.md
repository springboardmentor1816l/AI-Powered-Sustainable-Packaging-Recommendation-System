# Feature Engineering — EcoPackAI

## Overview
This document defines the formulas, assumptions and scoring strategies for three engineered indices:
- CO₂ Impact Index (CII)
- Cost Efficiency Index (CEI)
- Material Suitability Score (MSS)

Each index is scaled 0–100. Higher values mean:
- CII: **worse** environmental impact (higher CO₂ impact)
- CEI: **better** cost efficiency
- MSS: **more** suitable for general packaging use (unless product-specific overrides provided)

---

## Inputs (available / optional)
From `material_dataset.csv` (expected):
- `co2_emission_kg_per_kg` (float) — CO₂ kg emitted per kg of material
- `biodegradability_percent` (0–100) — share that biodegrades within target timeframe
- `recyclability_percent` (0–100)
- `cost_per_kg` (numeric)
- `strength_mpa` (numeric) — proxy for durability
- `weight_capacity_kg` (numeric) — proxy for load capacity
- Optional columns consumed if present:
  - `weight_required_kg` — packaging weight for a unit
  - `durability_score` — user-supplied 0–100 durability rating
  - `moisture_resistance`, `thermal_resistance` (0–100) — used for product-specific MSS

---

## Assumptions (if fields missing)
- If `weight_required_kg` missing, default `weight_required_kg = 0.1` kg per packaging unit (configurable).
- If biodegradation time not available, we use `biodegradability_percent` directly (higher = greener).
- If recyclability is present as percent, map to recyclability score = recyclability_percent / 100.
- All numeric inputs are clipped and normalized within dataset min/max before combining.

---

## 1) CO₂ Impact Index (CII)
**Goal:** Standardize environmental impact; higher = worse.

**Inputs:** `co2_emission_kg_per_kg`, `biodegradability_percent`, `recyclability_percent`.

**Steps (math):**
1. Normalize CO₂: `norm_co2 = (co2 - co2_min) / (co2_max - co2_min)` → range [0,1].
2. Biodeg score: `b = biodegradability_percent / 100` → higher = better.
3. Recycl score: `r = recyclability_percent / 100` → higher = better.
4. Combine using weights: `C_raw = w_co2*norm_co2 + w_b*(1 - b) + w_r*(1 - r)`, where:
   - `w_co2 = 0.6`, `w_b = 0.25`, `w_r = 0.15`.
   (We invert b and r because higher biodegradability/recyclability reduce impact.)
5. Scale: `CII = C_raw * 100` → range approx 0–100.

**Interpretation:** CII close to 100 = high CO₂ impact & poor biodegradability/recyclability.

---

## 2) Cost Efficiency Index (CEI)
**Goal:** Capture economic feasibility; higher = better.

**Inputs:** `cost_per_kg`, `weight_required_kg` (or default), `strength_mpa`, `recyclability_percent` (boost).

**Steps:**
1. Compute cost per unit: `cost_unit = cost_per_kg * weight_required_kg`.
2. Normalize cost_unit: `norm_cost = (cost_unit - min) / (max - min)`.
3. Durability proxy: `dur = min(1, strength_mpa / strength_max)` — normalized to [0,1].
4. Recycl boost: `rec = recyclability_percent / 100`.
5. Combine: `CE_raw = w_cost*(1 - norm_cost) + w_dur*dur + w_rec*rec`, where:
   - `w_cost = 0.70`, `w_dur = 0.20`, `w_rec = 0.10`.
6. Scale: `CEI = CE_raw * 100`.

**Interpretation:** CEI near 100 = low cost per unit, high durability, and recyclable.

---

## 3) Material Suitability Score (MSS)
**Goal:** Suitability of material for (general) packaging or specific product categories.

**Inputs:** `strength_mpa`, `weight_capacity_kg`, optional `moisture_resistance`, `thermal_resistance`, `product requirements`.

**Steps (general case):**
1. Normalize strength `s = (strength - min) / (max - min)`.
2. Normalize load `l = (weight_capacity - min) / (max - min)`.
3. Recyclability `rec = recyclability_percent / 100` (bonus).
4. MSS_raw = `w_s*s + w_l*l + w_rec*rec` where:
   - `w_s = 0.60`, `w_l = 0.30`, `w_rec = 0.10`.
5. Scale: `MSS = MSS_raw * 100`.

**Product-specific adjustments (if `product_requirements.csv` present):**
- Apply mandatory threshold checks (e.g., `s >= s_req`). If below, apply penalty (set MSS to MSS * 0.3 or subtract fixed penalty).
- Add attribute matching bonuses for moisture/thermal resistance.

---

## Final Recommendation Score (optional)
`Final_Score = alpha*(100 - CII) * + beta*CEI + gamma*MSS` (where `100 - CII` = environmental goodness). Default weights:
- `alpha = 0.4`, `beta = 0.3`, `gamma = 0.3`.

---

## Outputs
- Columns added to dataset:
  - `CII`, `CEI`, `MSS`, `final_recommendation_score`
- Feature metadata: JSON file documenting name, formula, inputs, range, direction.

---
