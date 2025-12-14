# EcoPackAI — Data Dictionary v2
**Module:** Save Processed Dataset & Document Schema

---

## Dataset-Level Summary

- Dataset name: materials_model_ready.parquet
- Number of rows: 404
- Number of columns: 35
- Dataset type: Production-ready ML dataset

### Feature Groups
- Raw attributes
- Encoded categorical features
- Scaled numerical features
- Sustainability & performance indicators

---

## Column-Level Details

| Column Name | Data Type | Description | Range / Categories | Example | Nullable | Derived | Used in ML |
|------------|----------|-------------|--------------------|--------|----------|---------|------------|
| Material ID | string | Unique material identifier | MAT_* | MAT_0001 | No | No | Yes |
| Packaging Type | float | Ordinal encoded packaging type | ≥ 0 | 2.0 | No | Yes | Yes |
| Material Type | float | Ordinal encoded material type | ≥ 0 | 1.0 | No | Yes | Yes |
| Supplier Region | float | Ordinal encoded region | ≥ 0 | 3.0 | No | Yes | Yes |
| Recyclability (%) | float | Recyclable portion | 0–100 | 75.0 | No | No | Yes |
| Carbon Footprint (kg CO2/unit) | float | Standard-scaled footprint | ℝ | -0.84 | No | Yes | Yes |
| Cost per Unit (USD) | float | Material cost | >0 | 2.75 | No | No | Yes |
| product_cat_* | int | Product category one-hot | {0,1} | 1 | No | Yes | Yes |
| usecase_* | int | Use case one-hot | {0,1} | 0 | No | Yes | Yes |
| Recyclability Category_High | int | Binary recyclability flag | {0,1} | 1 | No | Yes | Yes |

---

## Notes
- All percentage columns constrained to 0–100
- All encoded categorical features are numeric
- Dataset validated using automated unit tests

## Features & Targets

This section defines the **model input features (X)** and **target variables (y)** as identified in the **Define Target Variables & Features** stage.

> **Note:**  
> Target variables are **defined conceptually at this stage** and will be **materialized after feature engineering**.  
> This ensures proper sequencing and prevents target leakage.

---

### 1. Input Features (X)

#### Description
Input features represent **material characteristics, sustainability indicators, cost and usage metrics, performance scores, supplier attributes, and applicability signals** that are available *before* any recommendation decision is made.

These features are used as predictors for downstream machine learning models.

---

#### Feature Groups

| Feature Group | Description |
|-------------|-------------|
| Sustainability Metrics | Recyclability, waste reduction impact, carbon emissions |
| Performance Scores | Load handling, moisture resistance, thermal resistance |
| Cost & Usage Metrics | Cost per unit, annual usage, material weight |
| Lifecycle Indicators | Biodegradation time, end-of-life disposal |
| Supplier Attributes | Supplier sustainability compliance |
| Product Category Applicability | `product_cat_*` one-hot encoded indicators |
| Use Case Applicability | `usecase_*` one-hot encoded indicators |

---

#### Feature-Level Details (Representative)

| Feature Name | Data Type | Description | Range / Allowed Values | Nullable | Derived | Used in ML |
|------------|----------|-------------|-----------------------|----------|---------|------------|
| Recyclability (%) | Float | Percentage of recyclable content | 0–100 | No | No | Yes |
| Carbon Footprint (kg CO2/unit) | Float | Emissions per unit | ≥ 0 | No | No | Yes |
| Waste Reduction Impact (%) | Float | Reduction in material waste | 0–100 | No | No | Yes |
| Cost per Unit (USD) | Float | Cost of material per unit | > 0 | No | No | Yes |
| Load Handling Score | Integer | Structural load tolerance score | ≥ 0 | No | No | Yes |
| Supplier Sustainability Compliance (%) | Float | Supplier ESG compliance score | 0–100 | No | No | Yes |
| product_cat_* | Integer | Product category applicability flag | {0,1} | No | Yes | Yes |
| usecase_* | Integer | Use case applicability flag | {0,1} | No | Yes | Yes |

---

### 2. Target Variables (y)

#### Description
Target variables represent the **desired outcomes** that the model is expected to predict in later stages of the pipeline.

These targets are **not yet physically present in the dataset** at this stage and will be **materialized after feature engineering**.

---

#### Primary Target Variable

| Target Name | Type | Description | Derived | Used in ML |
|-----------|------|-------------|---------|------------|
| Final_Recommendation_Score | Regression (Continuous) | Overall recommendation score combining sustainability, cost efficiency, and suitability | Yes | Yes |

**Rationale:**  
This target enables ranking and recommendation of packaging materials based on a holistic evaluation of environmental and economic factors.

---

#### Secondary Target Variables (For Future Use)

| Target Name | Type | Description | Derived | Used in ML |
|-----------|------|-------------|---------|------------|
| CO2_Impact_Index | Regression | Composite environmental impact score | Yes | Later |
| Cost_Efficiency_Index | Regression | Economic efficiency score | Yes | Later |
| Material_Suitability_Score | Regression | Suitability of material for a specific product category | Yes | Later |

These secondary targets support:
- model explainability
- multi-objective optimization
- future multi-output learning setups

---

### 3. Feature–Target Separation (Leakage Prevention)

- Target variables are **explicitly excluded** from input features
- Identifier columns (e.g., `Material ID`) are excluded from modeling
- All input features represent information available *before* the decision outcome

This ensures **no target leakage** and preserves model validity.

---

### 4. Current Pipeline Status

| Component | Status |
|---------|--------|
| Input Features (X) | Materialized and saved |
| Target Variables (y) | Defined conceptually |
| Feature Engineering | Designed (next stage) |
| Model Training | Pending |

---

### Compliance Statement

The Features & Targets definition:
- follows best practices for ML pipeline design
- ensures clean separation of inputs and outputs
- is safe for downstream model development
