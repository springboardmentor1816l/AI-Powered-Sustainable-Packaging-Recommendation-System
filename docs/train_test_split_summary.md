# Train/Test Split Summary

## Overview

This document summarizes the train/test split strategy for the EcoPackAI dataset.

**Generated:** 2025-12-26 19:55:30

---

## Dataset Information

- **Source:** `data/processed/cleaned_integrated_materials.csv`
- **Total Samples:** 403
- **Features:** 20
- **Target Variables:** `cost_per_unit_usd`, `co2_emission_per_kg_estimated`

---

## Split Configuration

### Strategy: Stratified Train/Test Split

- **Train Size:** 322 samples (79.9%)
- **Test Size:** 81 samples (20.1%)
- **Stratification Column:** `material_type`
- **Random Seed:** 42
- **Shuffle:** True

### Rationale

The dataset is split using stratified sampling to ensure:

1. **Representative Distribution:** Both train and test sets maintain the same distribution of material types
2. **Unbiased Evaluation:** Test set accurately represents the population for fair model evaluation
3. **Reproducibility:** Fixed random seed enables exact replication of splits

---

## Distribution Analysis

### Material Type Distribution

| Material Type | Count | Percentage |
|--------------|-------|------------|
| Cardboard | 139 | 34.5% |
| Paper/Bio-Based | 37 | 9.2% |
| Plastic | 198 | 49.1% |
| Steel | 29 | 7.2% |

### Key Numeric Features

| Feature | Mean | Median | Std | Min | Max |
|---------|------|--------|-----|-----|-----|
| recyclability_percent | 91.61 | 94.00 | 8.59 | 55.00 | 100.00 |
| cost_per_unit_usd | 8.94 | 3.87 | 7.09 | 0.21 | 25.95 |
| co2_emission_per_kg_estimated | 1.15 | 1.40 | 0.72 | 0.28 | 3.25 |

---

## Data Integrity Validation

✅ All validation checks passed:

- No data loss between original and split datasets
- No overlap between training and testing sets
- Column consistency maintained across splits
- All material IDs preserved
- Target variables present in both splits
- Distribution similarity maintained

---

## Usage

```python
import pandas as pd
from sklearn.model_selection import train_test_split

# Load data
df = pd.read_csv('data/processed/cleaned_integrated_materials.csv')

# Recreate split
train_df, test_df = train_test_split(
    df,
    train_size=0.8,
    random_state=42,
    stratify=df['material_type'],
    shuffle=True
)
```
