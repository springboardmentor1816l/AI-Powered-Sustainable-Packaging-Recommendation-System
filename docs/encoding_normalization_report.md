# Materials DataSet
# Encoding and Normalization Report
---

## Encoding Strategy
1. **Nominal Categories** (Material Type, Supplier Region, Suitable Product Categories, Recommended Packaging Use Cases, Packaging Type, Recyclability Category): Used **One-Hot Encoding** (OHE) to create binary features for each unique category, as per the project plan. The fitted encoder object has been saved for reuse during model inference.

## Normalization Strategy
1. **Numeric Features** (Recyclability (%), Recycled Content (%), Reusability (%), Biodegradation Time (days), Carbon Footprint (kg CO2/unit), CO2 Emission per kg (estimated), Cost per Unit (USD), Waste Reduction Impact (%), Load Handling Score, Moisture Resistance Score, Thermal Resistance Score, Supplier Sustainability Compliance (%), Annual Usage (units), Total Material Weight (tons)): Used **MinMaxScaler** to scale all features to the range [0, 1]. This is suitable for features with different unit scales (e.g., percentages, scores, cost). The fitted scaler object has been saved for reuse during model inference.

## Validation (Final Encoded Dataset)
* **No missing values** remaining.
* **Numeric features** scaled between 0 and 1.
* **Categorical fields** successfully converted to numeric binary features.


# Products Dataset


# Products Dataset - Encoding and Normalization Report
---
## Encoding Strategy
1. **Nominal Categories** (category, shipping_type): Used **One-Hot Encoding** (OHE). The fitted encoder object has been saved for reuse during model inference.

## Normalization Strategy
1. **Numeric Features** (product_weight, fragility_index): Used **MinMaxScaler** to scale features to the range [0, 1]. The fitted scaler object has been saved for reuse during model inference.

## Validation (Final Encoded Dataset)
* **No missing values** remaining.
* **Numeric features** scaled between 0 and 1.
* **Categorical fields** successfully converted to numeric binary features.
