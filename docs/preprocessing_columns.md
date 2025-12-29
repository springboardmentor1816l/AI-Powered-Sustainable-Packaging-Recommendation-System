# Preprocessing Column Groups

This document defines the column groups used in the preprocessing pipeline.

## Numeric Features

These features undergo median imputation and standardization.

- `recyclability_percent`
- `recycled_content_percent`
- `reusability_percent`
- `biodegradation_time_days`
- `end_of_life_disposal_percent`
- `carbon_footprint_kg_co2_unit`
- `co2_emission_per_kg_estimated`
- `waste_reduction_impact_percent`
- `sustainability_target_progress_percent`
- `load_handling_score`
- `moisture_resistance_score`
- `thermal_resistance_score`
- `cost_per_unit_usd`
- `annual_usage_units`
- `total_material_weight_tons`
- `supplier_sustainability_compliance_percent`

## Categorical Features

These features undergo constant imputation (Unknown) and one-hot encoding.

- `packaging_type`
- `material_type`
- `supplier_region`
- `recyclability_category`

## Excluded Columns

These columns are not processed by the pipeline.

- `material_id`
- `suitable_product_categories`
- `recommended_packaging_use_cases`

## Summary

- **Total numeric features**: 16
- **Total categorical features**: 4
- **Total excluded columns**: 3
- **Total preprocessed features**: 20
