# 📦 Data Quality Report  
**EcoPackAI – Material Sustainability Dataset**  


## ✅ 1. Dataset Overview

The dataset contains **404 rows** and **23 columns**.

### **Feature Breakdown**
- **Numerical Features:** 20  
- **Categorical Features:** 3  
- **Primary Key:** `Material ID`  
  - 100% unique → **404 unique IDs out of 404 rows**

---

## ✅ 2. Missing Values Summary

Analysis of `missing_value_table.csv` reveals a clear pattern:

- **15 columns contain exactly 1 missing value each**, including:
  - Recycled Content  
  - Reusability  
  - Carbon Footprint  
  - Cost per Unit  
- Remaining columns have **0 missing values**.

### ✔ Interpretation
This pattern strongly indicates **a single corrupted row**, not random missing data.

---

## ✅ 3. Duplicate Records

- **Duplicate Rows:** 0  
- **Material ID Uniqueness:** Confirmed — 404 unique values.

Dataset integrity is strong.

---

## ✅ 4. Outlier Analysis

IQR-based outlier detection identified several extreme values:

### **High-Outlier Columns**
| Column | Outliers | Notes |
|--------|----------|-------|
| Carbon Footprint (kg CO₂/unit) | **59** | Wide variation due to material differences (Steel vs. PLA). |
| Total Material Weight (tons) | **46** | Reflects density or shipment volume differences. |
| Supplier Sustainability Compliance (%) | **30** | Some suppliers are very high/low. |
| Biodegradation Time (days) | **12** | Max ~180,208 days (~493 years) for non-biodegradable materials. |

---

## ✅ 5. Invalid Range Checks

| Column Type | Expected Range | Violations | Status |
|-------------|----------------|------------|--------|
| Percentages (Recyclability, Reusability) | 0–100 | 0 | ✔ Valid |
| Financials (Cost per Unit) | ≥ 0 | 0 | ✔ Valid |
| Emissions (Carbon Footprint) | ≥ 0 | 0 | ✔ Valid |

The dataset **strictly respects business logic constraints**.

---

## ✅ 6. Categorical Data Quality

- **Packaging Type:** 6 unique values  
- **Material Type:** 4 unique values  
- **Supplier Region:** 6 unique values  

---

## ✅ 7. Correlation Insights  
(From visual analysis performed in `EDA.ipynb`)

- A full **correlation heatmap** was generated.
- **Material Type distribution** visualization shows category balance.

---


✔ **End of Report**
