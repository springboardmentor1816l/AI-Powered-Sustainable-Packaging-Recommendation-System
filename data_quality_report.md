# EcoPackAI – Data Quality Report  
(Using EcoPackAI_dataset.csv)

## 1. Dataset Overview
- Total rows: **404**
- Total columns: **23**
- The dataset contains combined information about:
  - Material types  
  - Packaging categories  
  - Recyclability, reusability, biodegradation  
  - Cost, usage, weight  
  - Supplier sustainability  

---

## 2. Missing Values  
Only **3 columns** have missing values:

| Column                         | Missing | Percentage |
|-------------------------------|---------|------------|
| Recycled Content (%)          | 1       | 0.24%      |
| Reusability (%)               | 1       | 0.24%      |
| Biodegradation Time (days)    | 1       | 0.24%      |

### 🔹 Observations:
- Missing values are **very low (only 0.24%)**  
- Likely due to data entry gaps  
- These can be easily imputed with median values


## 3. Duplicate Records  
- Duplicate rows found: **0**  
- Dataset is clean with no repetition.

## 4. Outliers  
Possible outliers may exist in:

- **Cost per Unit (USD)**  
- **Annual Usage (units)**  
- **Total Material Weight (tons)**  
- **Biodegradation Time (days)**

## 5. Invalid or Inconsistent Values  
Based on a quick check:

- *No negative values detected* in numeric columns  
- *Recyclability (%) is between 0–100*  
- *Supplier Sustainability Compliance (%) is valid*  
- Category names appear consistent

---

## 6. Data Type Check
- Numeric columns:int64 / float64
- Categorical columns: object  
- All data types are correct and usable.

---

## 7. Recommended Cleaning Steps

### ✔ Handle Missing Values  
Use **median imputation** for:
- Recycled Content (%)  
- Reusability (%)  
- Biodegradation Time (days)  

### ✔ Treat Outliers  
- Use IQR capping for cost, usage, or weight  
- Outliers may be genuine but still need review  


### ✔ Convert Percent Fields  
Convert these to 0–1 scale if needed for ML:
- Recyclability (%)  
- Reusability (%)  
- Supplier Sustainability Compliance (%)  

---

## 8. Final Conclusion  
The dataset is very clean, with:
- Only *1 missing value* in three columns  
- No duplicates  
- Valid ranges  
- Good structure  


## 8. Findings & Next Steps

### 8.1 Missing Values
Only 3 columns contain missing values:
- Recycled Content (%): 1 missing
- Reusability (%): 1 missing
- Biodegradation Time (days): 1 missing

All other columns have 100% complete data.

### 8.2 Duplicates
- Duplicate rows: 0.
- Dataset is clean and unique.

### 8.3 Outliers
Potential outliers observed in:
- Cost per Unit (USD)
- Annual Usage (units)
- Biodegradation Time (days)
- Total Material Weight (tons)


### 8.4 Overall Data Quality
- Very high data quality  
- No invalid or negative values found  
- Percentages within valid range  
- Columns have correct data types

### 8.5 Next Steps (Cleaning Plan)
1. Impute the 3 missing values using median  
2. Apply IQR method for outlier treatment  
3. Standardize % columns if needed  
4. Proceed to feature engineering  

