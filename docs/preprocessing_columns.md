# Preprocessing Column Definitions
EcoPackAI – Product × Material Recommendation System

## 1. Excluded Columns (Not Used in Preprocessing)

These columns are excluded because they are identifiers, free-text fields, or
non-model features.

- **Material ID**  
  Reason: Unique identifier, not a predictive feature

- **product_id**  
  Reason: Unique identifier, not a predictive feature

- **product_name**  
  Reason: Free-text description, not encoded in this pipeline

- **Suitable Product Categories**  
  Reason: Descriptive text, overlaps with categorical features

- **Recommended Packaging Use Cases**  
  Reason: Free-text / advisory field, excluded from modeling

---

## 2. Numeric Features

These features are continuous or discrete numeric values related to product
characteristics, material sustainability, performance, and cost.

### Product Attributes
- product_weight_kg
- fragility_index

### Material Sustainability Metrics
- Recyclability (%)
- Recycled Content (%)
- Reusability (%)
- Biodegradation Time (days)
- End-of-Life Disposal (%)
- Carbon Footprint (kg CO2/unit)
- CO2 Emission per kg (estimated)
- Waste Reduction Impact (%)
- Sustainability Target Progress (%)

### Material Performance Metrics
- Load Handling Score
- Moisture Resistance Score
- Thermal Resistance Score

### Cost & Usage Metrics
- Cost per Unit (USD)
- Annual Usage (units)
- Total Material Weight (tons)
- Supplier Sustainability Compliance (%)

---

## 3. Categorical Features

These features represent discrete categories and are encoded using One-Hot Encoding.

### Product Attributes
- category
- shipping_type

### Material Attributes
- Packaging Type
- Material Type
- Recyclability Category
- Supplier Region

---

## 4. Binary Features

Currently, there are **no explicit binary (Yes/No) columns** in the dataset.
If added in the future (e.g., `Hazardous Material Flag`), they should be processed
using binary numeric encoding (0/1).

---
