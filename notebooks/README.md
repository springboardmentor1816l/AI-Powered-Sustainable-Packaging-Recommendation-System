# EcoPackAI Notebooks

This directory contains Jupyter notebooks for the **EcoPackAI** machine learning pipeline.

---

## 📓 Notebooks Overview

### 1. `01_dataset_prep.ipynb` - Dataset Preparation
**Status:** ✅ Completed  
**Purpose:** Define target variables and features for ML model  

**Key Tasks:**
- Load integrated materials dataset (404 rows)
- Define target variable: `material_type` (Cardboard, Paper/Bio-Based, Plastic, Steel)
- Identify 25 features across 5 categories
- Create X_raw (features) and y_raw (target)
- Generate feature metadata

**Outputs:**
- `data/ml_ready/X_raw.csv` - Feature matrix (404 × 25)
- `data/ml_ready/y_raw.csv` - Target variable (404 × 1)
- `data/ml_ready/feature_metadata.json` - Feature definitions

**Documentation:** See `docs/dataset_preparation_summary.md`

---

## 🚀 Quick Start

### Option 1: Run as Python Script
```powershell
# Execute the dataset preparation
python scripts/01_dataset_prep.py
```

### Option 2: Run as Jupyter Notebook
```powershell
# Start Jupyter
jupyter notebook

# Open 01_dataset_prep.ipynb
# Run all cells
```

---

## 📊 Feature Categories

| Category | Features | Type |
|----------|----------|------|
| Material Properties | 9 | Numeric |
| Packaging Requirements | 3 | Numeric |
| Cost & Operations | 4 | Numeric |
| Engineered Indices | 4 | Numeric |
| Categorical | 5 | Categorical |
| **Total** | **25** | **Mixed** |

---

## 🎯 Target Variable

- **Name:** `material_type`
- **Type:** Multi-class Classification
- **Classes:** 4 (Cardboard, Paper/Bio-Based, Plastic, Steel)
- **Distribution:** Balanced across categories

---

## 📁 Directory Structure

```
notebooks/
├── 01_dataset_prep.ipynb          # Dataset preparation notebook
├── README.md                       # This file
└── (future notebooks)
    ├── 02_feature_engineering.ipynb    # Feature engineering
    ├── 03_model_training.ipynb         # Model training
    ├── 04_model_evaluation.ipynb       # Model evaluation
    └── 05_model_deployment.ipynb       # Deployment preparation
```

---

## 📚 Related Documentation

- **Data Dictionary:** `docs/data_dictionary.md`
- **Dataset Prep Summary:** `docs/dataset_preparation_summary.md`
- **Project README:** `../README.md`

---

## 🔄 Next Steps

1. **Feature Engineering** - Create new features, interactions
2. **Data Encoding** - Encode categorical variables
3. **Data Scaling** - Normalize/standardize features
4. **Train-Test Split** - Split data for model training
5. **Model Training** - Train baseline ML models
6. **Model Evaluation** - Evaluate model performance

---

**Last Updated:** December 16, 2025  
**Version:** 1.0
