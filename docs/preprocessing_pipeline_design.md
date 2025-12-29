# Preprocessing Pipeline Design

## Overview

This document describes the preprocessing pipeline architecture and transformations applied to the EcoPackAI integrated dataset.

## Pipeline Architecture

The preprocessing pipeline uses scikit-learn's `ColumnTransformer` to apply different transformations to different feature types.

### Numeric Features Processing

**Transformation Steps:**
1. **Imputation**: Missing values are filled with the median
2. **Scaling**: Features are standardized (zero mean, unit variance)

**Columns (16):**
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

### Categorical Features Processing

**Transformation Steps:**
1. **Imputation**: Missing values are filled with 'Unknown'
2. **Encoding**: One-hot encoding is applied (creates binary columns)

**Columns (4):**
- `packaging_type`
- `material_type`
- `supplier_region`
- `recyclability_category`

### Output Features

After transformation, the pipeline produces **34 features**.

**Feature Name Examples:**
- `num__recyclability_percent`
- `num__recycled_content_percent`
- `num__reusability_percent`
- `num__biodegradation_time_days`
- `num__end_of_life_disposal_percent`
- `num__carbon_footprint_kg_co2_unit`
- `num__co2_emission_per_kg_estimated`
- `num__waste_reduction_impact_percent`
- `num__sustainability_target_progress_percent`
- `num__load_handling_score`
... and 24 more

## Usage

```python
import pickle

# Load the pipeline
with open('models/preprocessing/preprocessing_pipeline.pkl', 'rb') as f:
    preprocessor = pickle.load(f)

# Transform new data
X_transformed = preprocessor.transform(X_raw)
```

## Important Notes

- **Consistency**: The same pipeline must be used for training and inference
- **No Data Leakage**: Pipeline was fitted only on training data
- **Unknown Handling**: Categorical encoder handles unseen categories gracefully
- **Scalability**: Pipeline is serialized and can be loaded efficiently
