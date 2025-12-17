# EcoPackAI Data Dictionary

## Materials Table
- material_id (INT): Unique material identifier
- material_type (VARCHAR): Type of packaging material
- strength_mpa (FLOAT): Material strength
- biodegradability_percent (FLOAT): Biodegradability score
- recyclability_percent (FLOAT): Recycling potential
- cost_per_kg (FLOAT): Material cost
- industry_use_case (VARCHAR): Applicable industries

## Products Table
- product_id (INT): Unique product ID
- product_name (VARCHAR): Product name
- category (VARCHAR): Product category
- product_weight (FLOAT): Weight of product
- fragility_index (INT): Handling requirement
- shipping_type (VARCHAR): Shipping method

## Recommendation Logs
- rec_id (INT): Recommendation ID
- material_rank (INT): Rank of suggested material
- created_at (TIMESTAMP): Time of prediction
