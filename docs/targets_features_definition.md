
# AI Model Target and Feature Definition (Dec 12th)

This document formally defines the input (features) and output (targets) for the two parallel regression models in the EcoPackAI Recommendation System.

## 1. Target Variables (Model Outputs)

| Prediction Goal | Target Variable (y) | Data Type | Desired Direction |
| :--- | :--- | :--- | :--- |
| **Cost Prediction** | `Cost_Efficiency_Index` | Continuous (Scaled [0, 1]) | Lower is better (more cost-efficient) |
| **Environmental Prediction** | `CO2_Impact_Index` | Continuous (Scaled [0, 1]) | Lower is better (more sustainable) |

## 2. Final Feature Set (Model Inputs)

The final feature matrix (X) consists of all scaled, encoded, and engineered attributes from both the materials and products datasets, excluding the IDs and the target variables themselves.

**Total Features:** 57

### A. Material Features (Input Origin)
These 45 features are derived from the materials data, including all performance scores, engineered indices, and OHE material/supplier attributes.

* Recyclability (%)
* Recycled Content (%)
* Reusability (%)
* Biodegradation Time (days)
* Carbon Footprint (kg CO2/unit)
* CO2 Emission per kg (estimated)
* Cost per Unit (USD)
* Waste Reduction Impact (%)
* Load Handling Score
* Moisture Resistance Score
* Thermal Resistance Score
* Supplier Sustainability Compliance (%)
* Annual Usage (units)
* Total Material Weight (tons)
* Material_Suitability_Score
* Material Type_Cardboard
* Material Type_Paper/Bio-Based
* Material Type_Plastic
* Material Type_Steel
* Supplier Region_AMERICAS
* Supplier Region_APAC
* Supplier Region_EMEA
* Supplier Region_EU
* Supplier Region_LATAM
* Supplier Region_ROW
* Suitable Product Categories_E-commerce, Food & Beverage, Consumer Goods, Apparel
* Suitable Product Categories_Electronics, Medium-Value Goods, Retail Logistics
* Suitable Product Categories_Fragile Items, Cosmetics, Pharmaceuticals, Internal Component Protection
* Suitable Product Categories_Heavy Industrial Components, High-Security Goods
* Suitable Product Categories_Industrial Components, Heavy Machinery, Automotive Parts
* Suitable Product Categories_Low-Value Goods, Secondary Protection for Non-Fragile Items
* Recommended Packaging Use Cases_Closed-loop logistics and bulk material handling
* Recommended Packaging Use Cases_Cross-docking and returnable packaging programs
* Recommended Packaging Use Cases_Last-mile delivery and primary e-commerce packaging
* Recommended Packaging Use Cases_Secure, high-load international shipping and long-term storage
* Recommended Packaging Use Cases_Surface protection during transit; minimal void-fill
* Recommended Packaging Use Cases_Void-fill and cushioning for fragile products
* Packaging Type_Bubble Wrap (Minimal Use)
* Packaging Type_Cardboard Boxes
* Packaging Type_Foldable & Stackable Containers
* Packaging Type_Plastic Totes & Pallets
* Packaging Type_Protective Fillers (Paper/Biodegradable)
* Packaging Type_Steel Racks & Containers
* Recyclability Category_High
* Recyclability Category_Medium

### B. Product Features (Input Origin)
These 12 features are derived from the products data, including scaled physical properties and OHE category/shipping types.

* product_weight_kg
* fragility_index
* category_ Cosmetics
* category_Cosmetics
* category_Drinkware
* category_Electronics
* category_Food
* category_Paper Product
* category_Pharmacy
* shipping_type_Air
* shipping_type_Road
* shipping_type_Sea

