## ✅ 1. Mandatory Columns

All rows must contain valid values in the following columns:

* Material ID
* Recyclability (%)
* Recycled Content (%)
* Reusability (%)
* Biodegradation Time (days)
* End-of-Life Disposal (%)
* Carbon Footprint (kg CO2/unit)
* CO2 Emission per kg (estimated)
* Waste Reduction Impact (%)
* Sustainability Target Progress (%)
* Load Handling Score
* Moisture Resistance Score
* Thermal Resistance Score
* Cost per Unit (USD)
* Annual Usage (units)
* Total Material Weight (tons)
* Supplier Sustainability Compliance (%)

---

##  2. One‑Hot Encoded Packaging Type Columns

Values must be **0 or 1 only**.

* Packaging Type_Bubble Wrap (Minimal Use)
* Packaging Type_Cardboard Boxes
* Packaging Type_Foldable & Stackable Containers
* Packaging Type_Plastic Totes & Pallets
* Packaging Type_Protective Fillers (Paper/Biodegradable)
* Packaging Type_Steel Racks & Containers

At least **one of these must be 1** per row.

---

##  3. One‑Hot Encoded Material Type Columns

Values must be **0 or 1 only** and exactly **one must be 1**:

* Material Type_Cardboard
* Material Type_Paper/Bio-Based
* Material Type_Plastic
* Material Type_Steel

---

## 4. Recyclability Category Columns

One-hot encoded — values must be 0 or 1.

* Recyclability Category_High
* Recyclability Category_Medium

Exactly **one category must be 1**.

---

## 5. Supplier Region Columns

Must be one-hot encoded, values 0 or 1:

* Supplier Region_AMERICAS
* Supplier Region_APAC
* Supplier Region_EMEA
* Supplier Region_EU
* Supplier Region_LATAM
* Supplier Region_ROW

Exactly **one must be 1**.

---

## 6. Suitable Product Categories (One‑Hot Encoded)

Values: **0 or 1**.

* Suitable Product Categories_E-commerce, Food & Beverage, Consumer Goods, Apparel
* Suitable Product Categories_Electronics, Medium-Value Goods, Retail Logistics
* Suitable Product Categories_Fragile Items, Cosmetics, Pharmaceuticals, Internal Component Protection
* Suitable Product Categories_Heavy Industrial Components, High-Security Goods
* Suitable Product Categories_Industrial Components, Heavy Machinery, Automotive Parts
* Suitable Product Categories_Low-Value Goods, Secondary Protection for Non-Fragile Items

At least **one must be 1** per row.

---

##  7. Recommended Packaging Use Cases (One‑Hot)

Values: **0 or 1**.

* Recommended Packaging Use Cases_Closed-loop logistics and bulk material handling
* Recommended Packaging Use Cases_Cross-docking and returnable packaging programs
* Recommended Packaging Use Cases_Last-mile delivery and primary e-commerce packaging
* Recommended Packaging Use Cases_Secure, high-load international shipping and long-term storage
* Recommended Packaging Use Cases_Surface protection during transit; minimal void-fill
* Recommended Packaging Use Cases_Void-fill and cushioning for fragile products

At least **one must be 1** per row.

---

##  8. Numeric Value Constraints

All numeric fields follow these rules:

### Must be ≥ 0

* Recyclability (%)
* Recycled Content (%)
* Reusability (%)
* Biodegradation Time (days)
* End-of-Life Disposal (%)
* Carbon Footprint (kg CO2/unit)
* CO2 Emission per kg (estimated)
* Waste Reduction Impact (%)
* Sustainability Target Progress (%)
* Load Handling Score
* Moisture Resistance Score
* Thermal Resistance Score
* Cost per Unit (USD)
* Annual Usage (units)
* Total Material Weight (tons)
* Supplier Sustainability Compliance (%)

### Expected Ranges

* Load Handling Score: **0–1**
* Moisture Resistance Score: **0–1**
* Thermal Resistance Score: **0–1**
* One-hot encoded columns: **0 or 1** only

---

##  9. Integrity & Uniqueness Rules

* **Material ID must be unique**
* No duplicate rows
* No negative values in numeric fields

---
