# Feature Engineering Document
This document explains how engineered features were created for the EcoPackAI recommendation and scoring system. These features help quantify sustainability, cost efficiency, and material suitability.

---

## 1. CO₂ Impact Index (CII)
**Goal:** Measure environmental impact of each material (0–100 scale).

### Inputs Used
- co2_emission_score (normalized 0–1)
- biodegradability_percent (0–1)
- recyclability_percent (0–1)

### Logic
- Lower CO₂ emissions = better score  
- Higher biodegradability = better score  
- Higher recyclability = better score  

### Formula (conceptual)

---

## 2. Cost Efficiency Index (CEI)
**Goal:** Represent economic feasibility of using a material (0–100 scale).

### Inputs Used
- cost_per_kg (0–1 normalized)
- strength_mpa
- durability aspects encoded in dataset

### Logic
- Lower cost materials score higher
- Stronger materials receive a small positive contribution

### Formula (conceptual)

---

## 3. Material Suitability Score (MSS)
**Goal:** Measure how suitable a material is in general for packaging applications (0–100 scale).

### Inputs Used
- strength_mpa  
- weight_capacity  
- recyclability_percent  

### Logic
- Strong & durable materials score higher  
- Recyclability contributes positively  

### Formula (conceptual)

---

# Engineered Features Summary

| Feature | Description | Range | Purpose |
|---------|-------------|--------|---------|
| CII | CO₂ Impact Index | 0–100 | Sustainability assessment |
| CEI | Cost Efficiency Index | 0–100 | Cost feasibility |
| MSS | Material Suitability Score | 0–100 | Material performance evaluation |

