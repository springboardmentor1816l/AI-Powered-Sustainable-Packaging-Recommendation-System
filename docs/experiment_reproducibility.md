# Experiment Reproducibility Guide

## Overview

This document provides all necessary information to reproduce the exact train/test splits and cross-validation folds used in the EcoPackAI project.

---

## Critical Parameters

### Random Seeds

**Master Random Seed:** `42`

This seed is used for:
- Train/test splitting
- Cross-validation fold generation
- Any stochastic operations in preprocessing

### Software Versions

- **Python:** 3.8+
- **scikit-learn:** scikit-learn>=1.0.0
- **pandas:** >=1.3.0
- **numpy:** >=1.21.0

### Dataset Version

- **Source File:** `data/processed/cleaned_integrated_materials.csv`
- **Total Samples:** 403
- **Creation Date:** 2025-12-26T19:55:30.475479

---

## Reproduction Steps

### Step 1: Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install scikit-learn>=1.0.0 pandas>=1.3.0 numpy>=1.21.0
```

### Step 2: Load Dataset

```python
import pandas as pd

df = pd.read_csv('data/processed/cleaned_integrated_materials.csv')
assert len(df) == 403, 'Dataset size mismatch'
```

### Step 3: Reproduce Train/Test Split

```python
from sklearn.model_selection import train_test_split

train_df, test_df = train_test_split(
    df,
    train_size=0.7990074441687345,
    random_state=42,
    stratify=df['material_type'],
    shuffle=True
)

assert len(train_df) == 322
assert len(test_df) == 81
```

### Step 4: Reproduce Cross-Validation Folds

```python
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
stratify_labels = le.fit_transform(train_df['material_type'])

skf = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

for fold_idx, (train_idx, val_idx) in enumerate(skf.split(train_df, stratify_labels), 1):
    print(f'Fold {fold_idx}: Train={len(train_idx)}, Val={len(val_idx)}')
```

---

## Validation Checklist

After reproducing the splits, verify:

- [ ] Train set size matches expected count
- [ ] Test set size matches expected count
- [ ] No overlap between train and test sets
- [ ] Stratification distributions match
- [ ] All CV folds have expected sizes
- [ ] Material type distributions are preserved

---

## Important Notes

1. **Exact Reproducibility:** Using the specified random seed with the same sklearn version guarantees identical splits

2. **Dataset Integrity:** The source dataset must not be modified. Any changes will result in different splits

3. **Version Consistency:** Different scikit-learn versions may produce different random sequences. Use the specified version for exact reproduction

4. **No Test Set Contamination:** The test set should never be used during model development, hyperparameter tuning, or cross-validation

---

## Metadata Reference

Complete split metadata is stored in: `ml/metadata/split_metadata.json`

This file contains:
- Exact split counts and percentages
- Distribution statistics for all folds
- Dataset feature information
- All random seeds and configuration parameters
