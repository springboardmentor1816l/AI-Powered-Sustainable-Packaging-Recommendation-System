# Feature Engineering Document
Project: EcoPackAI – Sustainable Packaging Recommendation System

## Overview
This document defines the engineered features used to convert raw packaging material attributes into standardized sustainability, cost, and suitability metrics. These features enable fair comparison, ranking, and ML-based recommendations.

---

## 1. CO₂ Impact Index (CII)

### Purpose
Quantifies the environmental impact of packaging materials by combining emissions, biodegradability, and recyclability.

### Inputs
- CO₂ Emission per kg
- Biodegradation Time (days)
- Recyclability Category (A, B, C, D)
- Material Type

### Logic
- CO₂ emissions are normalized (0–1), lower emissions score higher.
- Biodegradation time is converted into a green score where faster degradation increases score.
- Recyclability categories are mapped:
  - A → 1.0
  - B → 0.75
  - C → 0.5
  - D → 0.25
- Material-type-based sustainability weight is applied.

### Output
- CO₂ Impact Index (0–100)
- Higher value = more environmentally friendly

---

## 2. Cost Efficiency Index (CEI)

### Purpose
Measures economic feasibility of packaging materials over their lifecycle.

### Inputs
- Cost per unit
- Material durability score
- Recyclability percentage
- Reusability percentage
- Weight required per unit packaging

### Logic
- Cost per unit is normalized.
- High durability and reusability increase score.
- High recyclability reduces long-term cost.
- Penalizes materials with high cost but low durability.

### Output
- Cost Efficiency Index (0–100)
- Higher value = more cost-effective

---

## 3. Material Suitability Score (MSS)

### Purpose
Evaluates how well a material matches product packaging requirements.

### Inputs
- Load Handling Score
- Moisture Resistance Score
- Thermal Resistance Score
- Product Category Requirements
- Material Safety Compatibility

### Logic
- Material attributes are compared against product sensitivity thresholds.
- Mandatory failures (e.g., low heat resistance for hot products) apply penalties.
- High alignment earns bonus points.
- Category-specific weight matrix is applied.

### Output
- Material Suitability Score (0–100)
- Higher value = better suitability

---

## Final Notes
These engineered features form the foundation for:
- ML ranking models
- Recommendation engines
- Sustainability dashboards
