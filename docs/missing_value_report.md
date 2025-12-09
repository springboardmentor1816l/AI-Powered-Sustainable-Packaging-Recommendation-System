
# Missing Value Report
---

## Summary of Missing Values

| Column | Missing Count | Strategy |
| :--- | :--- | :--- |
| Recycled Content (%) | 1 | Median Imputation (Numeric)
| Reusability (%) | 1 | Median Imputation (Numeric)
| Biodegradation Time (days) | 1 | Median Imputation (Numeric)
| Carbon Footprint (kg CO2/unit) | 1 | Median Imputation (Numeric)
| CO2 Emission per kg (estimated) | 1 | Median Imputation (Numeric)
| Cost per Unit (USD) | 1 | Median Imputation (Numeric)
| Waste Reduction Impact (%) | 1 | Median Imputation (Numeric)
| Load Handling Score | 1 | Median Imputation (Numeric)
| Moisture Resistance Score | 1 | Median Imputation (Numeric)
| Thermal Resistance Score | 1 | Median Imputation (Numeric)
| Supplier Sustainability Compliance (%) | 1 | Median Imputation (Numeric)
| Annual Usage (units) | 1 | Median Imputation (Numeric)
| Total Material Weight (tons) | 1 | Median Imputation (Numeric)

## Decisions
1. **Numeric (continuous) features** (Strength, Cost, CO2, etc.): Impute using the **Median** strategy to minimize the impact of potential outliers, as per the project plan[cite: 218].
2. **Categorical features** (Material Type, Industry Use Case): Impute using the **Mode (most frequent)** strategy, although no missing values were detected in these columns in the current raw dataset.
3. **No rows were removed** as the percentage of missing data (approx. 5%) was low and spread across columns.
