## 1. Objective

This report summarizes the transformation of the cleaned dataset into a **machine-learning-ready format**.  
Steps included:

1. Encoding categorical features  
2. Normalizing numeric features  
3. Saving encoders and scalers for reuse during inference  

---

## 2. Categorical Features

### Columns Encoded
| Column Name | Encoding Type |
|-------------|---------------|
| Packaging Type | One-Hot Encoding (Nominal) |
| Material Type | One-Hot Encoding (Nominal) |
| Recyclability Category | One-Hot Encoding (Nominal) |
| Supplier Region | One-Hot Encoding (Nominal) |
| Suitable Product Categories | One-Hot Encoding (Nominal) |
| Recommended Packaging Use Cases | One-Hot Encoding (Nominal) |

**Details:**

- **Method:** One-Hot Encoding using `sklearn.preprocessing.OneHotEncoder`  
- **Handle Unknown Categories:** `handle_unknown='ignore'` ensures new unseen categories can be safely handled during prediction.  
- **Output:** New binary columns representing each category level.  

**Encoder Saved:**  
`models/encoders/ohe_encoder.pkl`  

---

## 3. Numeric Features

### Columns Normalized
| Column Name |
|-------------|
| Recyclability (%) |
| Recycled Content (%) |
| Reusability (%) |
| Biodegradation Time (days) |
| End-of-Life Disposal (%) |
| Carbon Footprint (kg CO2/unit) |
| CO2 Emission per kg (estimated) |
| Waste Reduction Impact (%) |
| Sustainability Target Progress (%) |
| Load Handling Score |
| Moisture Resistance Score |
| Thermal Resistance Score |
| Cost per Unit (USD) |
| Annual Usage (units) |
| Total Material Weight (tons) |
| Supplier Sustainability Compliance (%) |

**Exclusions:**  
- `Material ID` was **not scaled** as it is a unique identifier.  

**Method:**  
- **Min-Max Scaling** using `sklearn.preprocessing.MinMaxScaler`  
- **Range:** All numeric values transformed to **[0, 1]**  
- **Reason:** Different numeric features have varying units and scales. Normalization ensures uniform scale for ML models.

**Scaler Saved:**  
`models/scalers/numeric_scaler.pkl`  

---

## 4. Combined ML-Ready Dataset

- All numeric columns are scaled.  
- All categorical columns are One-Hot encoded.  
- Original `Material ID` is preserved.  
- Dataset saved as:  
`data/model_ready/materials_final_encoded.csv`  

---

## 5. File/Folder Summary

| File/Folder | Description |
|-------------|-------------|
| `data/processed/cleaned_integrated_materials.csv` | Cleaned dataset after missing value imputation |
| `data/model_ready/materials_final_encoded.csv` | Encoded and normalized dataset for ML |
| `models/encoders/ohe_encoder.pkl` | One-Hot Encoder for categorical columns |
| `models/scalers/numeric_scaler.pkl` | MinMax Scaler for numeric columns |
| `docs/missing_value_report.md` | Summary of missing value handling |
| `docs/encoding_normalization_report.md` | This report |

---
