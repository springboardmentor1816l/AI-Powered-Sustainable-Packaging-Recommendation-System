### EcoPackAI — Sustainability & Performance Feature Definitions

---

## **1. CO₂ Impact Index (CII)**

### **Goal:**

Standardize environmental impact of materials using CO₂ emissions, biodegradation time, and recyclability.

### **Inputs Required:**

* `CO2_emissions_per_kg`
* `biodegradation_time_days`
* `recyclability_category` (A/B/C/D)
* `material_type`

### **Scoring Logic:**

1. **Normalize CO₂ emissions** (0–1 scale):

   * `CO2_norm = (CO2 - CO2_min) / (CO2_max - CO2_min)`
2. **Normalize biodegradation time:**

   * `BD_norm = (BD - BD_min) / (BD_max - BD_min)`
3. **Convert recyclability category:**

   * A=1.00, B=0.75, C=0.50, D=0.25
4. **Material sustainability weight:**

   * Bio-based: +0.10
   * Paper: +0.05
   * Metal: 0
   * Plastic: −0.10

### **Formula:**

```
CII_raw = (0.4 * (1 - CO2_norm)) +
          (0.3 * (1 - BD_norm)) +
          (0.3 * recyclability_score)

CII = CII_raw * 100
```

---

## **2. Cost Efficiency Index (CEI)**

### **Goal:**

Understand economic feasibility of using each material.

### **Inputs:**

* `cost_per_kg`
* `weight_required`
* `recyclability`
* `durability_score`

### **Scoring Logic:**

1. Normalize cost (low cost = high score)
2. Compute per-package material cost
3. Add bonus for recyclable materials
4. Penalize low durability

### **Formula:**

```
cost_unit = cost_per_kg * weight_required

CEI_raw = (0.5 * (1 - cost_norm)) +
          (0.2 * durability_norm) +
          (0.3 * recyclability_score)

CEI = CEI_raw * 100
```

---

## **3. Material Suitability Score (MSS)**

### **Goal:**

Define how appropriate a material is for a given product category.

### **Inputs:**

* `load_handling`
* `moisture_resistance`
* `thermal_resistance`
* `durability`
* `product_category`
* `material_type`

### **Logic:**

1. Match material attributes to product requirements
2. Mandatory requirement failure results in penalty
3. Add bonus for over-performance
4. Combine weighted attributes

### **Formula:**

```
MSS_raw = (0.25 * load_score) +
          (0.25 * moisture_score) +
          (0.20 * thermal_score) +
          (0.20 * durability_score) +
          (0.10 * category_match_weight)

MSS = MSS_raw * 100
```

---
