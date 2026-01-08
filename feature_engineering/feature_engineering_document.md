# Feature Engineering Document – EcoPackAI

## Overview
This document explains the engineered sustainability and performance features created from raw packaging material data. These features improve decision-making, recommendation accuracy, and ML readiness.

---

## 1. CO₂ Impact Index (CII)

### Objective
To quantify the environmental sustainability of packaging materials by combining emissions, biodegradability, and recyclability.

### Inputs Used
- CO₂ emissions per kg
- Biodegradation time (days)
- Recyclability category (A, B, C, D)
- Material type

### Feature Engineering Logic
1. CO₂ emissions are normalized to a 0–1 scale.
2. Biodegradation time is converted into a green impact score (faster degradation = higher score).
3. Recyclability categories are mapped:
   - A = 1.0
   - B = 0.75
   - C = 0.50
   - D = 0.25
4. Sustainability weights are applied based on environmental guidelines.
5. All components are combined to produce a final index.

### Output
- CO₂ Impact Index (Range: 0–100)
- Higher value indicates better environmental sustainability.

---

## 2. Cost Efficiency Index (CEI)

### Objective
To measure the economic feasibility of using a particular packaging material.

### Inputs Used
- Cost per kg
- Packaging weight requirement
- Recyclability
- Material durability score

### Feature Engineering Logic
1. Cost-related inputs are standardized.
2. Cost per unit packaging is calculated.
3. Recyclable or reusable materials receive an efficiency bonus.
4. High-cost and low-durability materials receive a penalty.
5. Final score reflects overall cost efficiency.

### Output
- Cost Efficiency Index (Range: 0–100)
- Higher value indicates better cost performance.

---

## 3. Material Suitability Score (MSS)

### Objective
To evaluate how suitable a packaging material is for a specific product category.

### Inputs Used
- Load handling score
- Moisture resistance score
- Thermal resistance score
- Durability rating
- Product category requirements
- Material safety suitability

### Feature Engineering Logic
1. Material attributes are matched with product requirements.
2. Mandatory requirement failures result in penalties.
3. High alignment with product sensitivity earns bonuses.
4. Category-specific weight matrices are applied.

### Output
- Material Suitability Score (Range: 0–100)
- Higher value indicates better suitability.

---

## Conclusion
These engineered features form the foundation of EcoPackAI’s recommendation engine and sustainability scoring system.
