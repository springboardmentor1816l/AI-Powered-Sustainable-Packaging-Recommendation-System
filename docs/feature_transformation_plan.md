# Feature Transformation Plan — Steps to compute features

## Requirements
- Python 3.8+
- pandas, numpy
- Input file: `data/material_dataset.csv`
- Optional: `data/product_requirements.csv` (category-level thresholds)

## Steps (script flow)
1. Load `material_dataset.csv` into DataFrame `df`.
2. Ensure required numeric columns exist; fill missing with safe defaults and log.
3. Add `weight_required_kg` default 0.1 if not present.
4. Compute auxiliary normalized columns using min/max across dataset:
   - `norm_co2`, `norm_cost_unit`, `norm_strength`, `norm_capacity`.
5. Compute CII, CEI, MSS as specified in the document.
6. Clip final indices into [0,100].
7. Optionally compute `final_recommendation_score` using default weights.
8. Export:
   - `data/materials_featured.csv` (updated dataset)
   - `feature_metadata.json`
   - brief `feature_engineering_log.txt` summarizing min/max used.
