# Data Dictionary v2

This document describes all fields in the updated materials and products datasets.

---

# MATERIALS DATASET

| Column | Type | Description | Range | Nullable | Derived | ML Use |
|--------|------|-------------|--------|----------|---------|--------|
| material_id | string | Unique material identifier | — | No | No | Yes |
| strength_mpa | float | Material strength score | 0–1 | No | No | Yes |
| weight_capacity | float | Normalized weight handling | 0–1 | No | No | Yes |
| biodegradability_percent | float | Biodegradability (normalized) | 0–1 | No | No | Yes |
| co2_emission_score | float | CO₂ emission score | 0–1 | No | No | Yes |
| recyclability_percent | float | Recyclability | 0–1 | No | No | Yes |
| cost_per_kg | float | Material cost | >0 | No | No | Yes |
| CII | float | CO₂ Impact Index | 0–100 | No | Yes | Yes |
| CEI | float | Cost Efficiency Index | 0–100 | No | Yes | Yes |
| MSS | float | Material Suitability Score | 0–100 | No | Yes | Yes |

---

# PRODUCTS DATASET

| Column | Type | Description | Range | Nullable | Derived | ML Use |
|--------|------|-------------|--------|----------|---------|--------|
| product_id | string | Unique product identifier | — | No | No | Yes |
| product_weight | float | Weight of product | ≥0 | No | No | Yes |
| fragility_index | float | Fragility score | ≥0 | No | No | Yes |
| required_load | int | Required load handling | 1–10 | No | Yes | Yes |
| required_moisture | int | Required moisture resistance | 1–10 | No | Yes | Yes |
| required_thermal | int | Required thermal resistance | 1–10 | No | Yes | Yes |
| category_* | int | One-hot categories | 0/1 | No | No | Yes |
| shipping_type_* | int | One-hot category | 0/1 | No | No | Yes |

