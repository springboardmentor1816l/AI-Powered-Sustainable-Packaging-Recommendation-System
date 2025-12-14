# EcoPackAI — Feature Engineering Document
**Module:** Feature Engineering

## Objective
The objective of this phase is to derive meaningful, explainable composite
features from existing material sustainability and cost attributes to support
decision-making and downstream machine learning models.

The following engineered features were created:
- CO₂ Impact Index (CII)
- Cost Efficiency Index (CEI)
- Material Suitability Score (MSS)
- Final Recommendation Score (FRS)

All indices are normalized to a 0–100 scale.

Base dataset used:
`cleaned_integrated_materials.csv`

---

## 1. CO₂ Impact Index (CII)

### Description
The CO₂ Impact Index represents the overall environmental impact of a material
based on emissions, degradation behavior, and recyclability.

### Contributing Features
- Carbon Footprint
- Biodegradation Time (days)
- Recyclability Category
- Material Type

### Recyclability Mapping (Decimal)
| Category | Score |
|--------|-------|
| A | 1.00 |
| B | 0.75 |
| C | 0.50 |
| D | 0.25 |

### Weighting Strategy (Expert-defined)
- Carbon Footprint: 40%
- Biodegradation Time: 30%
- Recyclability Score: 20%
- Material Type Factor: 10%

### Interpretation
- Higher CII → higher environmental impact
- Lower CII → more sustainable material

---

## 2. Cost Efficiency Index (CEI)

### Description
The Cost Efficiency Index measures how economically viable a material is when
considering cost, durability, and recyclability.

### Contributing Features
- Cost per kg
- Weight Capacity
- Recyclability Category

### Weighting Strategy
- Cost per kg: 50%
- Weight Capacity: 30%
- Recyclability Score: 20%

### Interpretation
- Higher CEI → more cost-efficient material

---

## 3. Material Suitability Score (MSS)

### Description
The Material Suitability Score evaluates how suitable a material is for a given
product category based on functional and sustainability requirements.

### Scope
Computed **per (material × product category)**.

### Contributing Features
- Strength / Weight Capacity
- Biodegradability
- Recyclability
- Product Category Requirements (assumed mapping)

### Product Category Matching
A documented compatibility matrix was used to align:
- Material properties
- Product category needs (e.g., fragile, food-safe, durable)

### Interpretation
- Higher MSS → better suitability for the target product category

---

## 4. Final Recommendation Score (FRS)

### Description
The Final Recommendation Score provides a single composite score to rank
materials holistically.

### Formula
FRS = weighted average of:
- CO₂ Impact Index
- Cost Efficiency Index
- Material Suitability Score

### Interpretation
- Higher FRS → better overall recommendation

---

## Summary
The engineered features improve interpretability, decision support, and model
performance while remaining explainable and auditable.
