# 🏆 Packaging Material Ranking Logic

## Overview

EcoPackAI ranks packaging materials by analyzing **product-specific inputs** and computing a **composite score** for each material. The ranking ensures an optimal balance between **cost, environmental impact, and sustainability**, while maintaining product safety during shipping.

---

## 🔹 Input Parameters (Product Details)

The ranking logic uses the following inputs provided by the user:

* **Product Name** – Identifies the product (used for report labeling and domain reference)
* **Category** – Determines industry-specific packaging suitability
* **Weight (kg)** – Influences material strength and thickness requirements
* **Fragility Index** – Indicates protection level required (0.0 = low, 1.0 = high)
* **Shipping Type** – Defines logistics conditions (Air, Road, Sea)

---

## 🔹 Step 1: Material Feasibility Filtering

Before ranking, EcoPackAI filters out unsuitable materials based on **minimum feasibility rules**:

### Filtering Criteria:

1. **Weight Capacity**
   - Materials unable to support the given weight are removed
   - Example: Kraft Paper (max 8kg) filtered out for 10kg products

2. **Fragility Requirements**
   - Fragile products eliminate materials with insufficient cushioning
   - High fragility (>0.7) requires materials with fragility_bonus ≥ 5

3. **Shipping Type Compatibility**
   - Materials unsuitable for specific shipping methods are removed
   - Example: PLA not recommended for Sea shipping (moisture issues)

Only **feasible materials** proceed to scoring.

---

## 🔹 Step 2: Attribute Scoring per Material

Each remaining packaging material is evaluated using three measurable attributes:

### 1️⃣ Cost Score

**Formula:**
```
cost_score = 100 - (actual_cost / max_cost * 100)
```

**Where:**
- `actual_cost` = base_cost + fragility_adjustment
- `base_cost` = product_weight × material_cost_factor × 45
- `fragility_adjustment` = fragility_index × (40 - fragility_bonus)

**Result:** Lower cost → Higher score (0-100)

---

### 2️⃣ CO₂ Impact Score

**Formula:**
```
co2_score = 100 - (actual_co2 / max_co2 * 100)
```

**Where:**
- `actual_co2` = product_weight × shipping_multiplier × 2.0 × co2_factor
- Shipping multipliers:
  - Air: 3.5 (highest emissions)
  - Road: 1.5 (medium emissions)
  - Sea: 0.8 (lowest emissions)

**Result:** Lower CO₂ → Higher score (0-100)

---

### 3️⃣ Sustainability Score

**Formula:**
```
sustainability_score = (recyclability × 0.4) + (biodegradability × 0.4) + (renewability × 0.2)
```

**Components:**
- **Recyclability** (40%): Can the material be recycled?
- **Biodegradability** (40%): How quickly does it decompose naturally?
- **Renewability** (20%): Is it made from renewable resources?

**Result:** Higher values indicate better sustainability (0-100)

---

## 🔹 Step 3: Weighted Composite Score Calculation

A **weighted scoring formula** is applied to compute the final score for each material:

### Formula:
```
Final Score = (0.50 × Sustainability) + (0.30 × CO₂ Impact) + (0.20 × Cost)
```

### Weight Distribution:

| Factor         | Weight | Priority | Rationale                                    |
|----------------|--------|----------|----------------------------------------------|
| Sustainability | 50%    | 1st      | Highest priority - long-term environmental impact |
| CO₂ Impact     | 30%    | 2nd      | Climate change mitigation                    |
| Cost           | 20%    | 3rd      | Economic optimization without compromising sustainability |

**Why this distribution?**
- Sustainability gets highest weight (50%) to prioritize long-term environmental goals
- CO₂ impact (30%) addresses immediate climate concerns
- Cost (20%) ensures economic viability while maintaining green standards

---

## 🔹 Step 4: Ranking Logic

Materials are sorted based on their **Final Score**:

1. **Highest score** = **Rank #1** (Best recommendation)
2. Materials sorted in **descending order**
3. Top N materials returned (configurable, default = 4)

### Ranking Example:

| Rank | Material                 | Cost  | CO₂   | Sustainability | Final Score |
|------|--------------------------|-------|-------|----------------|-------------|
| 1    | Bio-Plastic (Cornstarch) | ₹52.8 | 3.84  | 92.5           | 87.3        |
| 2    | PLA (Polylactic Acid)    | ₹72.0 | 3.36  | 91.7           | 85.6        |
| 3    | Recycled Cardboard       | ₹45.0 | 6.24  | 84.3           | 79.2        |
| 4    | Kraft Paper              | ₹36.0 | 5.28  | 82.8           | 78.5        |

---

## 🔹 Step 5: Output Generation

The final ranked output is displayed with:

- **Rank**: Position in the recommendation list
- **Material**: Name of packaging material
- **Cost**: Estimated cost (₹)
- **CO₂ Impact**: Carbon emissions (kg CO₂ equivalent)
- **Sustainability Score**: Final composite score (0-100)

### Output Features:

✅ **Explainable Rankings** - Users understand why each material is ranked
✅ **Transparent Trade-offs** - Clear view of cost vs. environmental impact
✅ **Actionable Insights** - Easy decision-making based on priorities

---

## 🔧 Configuration

Ranking parameters can be adjusted in `config/ranking_weights.yaml`:

```yaml
weights:
  sustainability: 0.50  # Adjust priority weights
  co2_impact: 0.30
  cost: 0.20

constraints:
  max_cost: 200         # Maximum acceptable cost
  min_recyclability: 50 # Minimum recyclability %
  max_co2: 20          # Maximum CO₂ emissions (kg)

top_n: 4               # Number of recommendations
```

---

## ✅ Result Summary

This ranking logic ensures that:

✓ Packaging is **safe for the product** (feasibility filtering)
✓ Environmental impact is **minimized** (sustainability priority)
✓ Sustainability goals are **prioritized** (50% weight)
✓ Cost is **optimized** without compromising green standards
✓ Businesses receive **transparent, ranked recommendations**

---

## 📊 Algorithm Complexity

- **Time Complexity**: O(n log n) where n = number of materials
  - Filtering: O(n)
  - Scoring: O(n)
  - Sorting: O(n log n)

- **Space Complexity**: O(n) for storing material scores

---

## 🎯 Use Cases

1. **E-commerce Businesses**: Optimize packaging for online orders
2. **Food Industry**: Prioritize biodegradable materials for perishables
3. **Electronics Manufacturers**: Balance protection with sustainability
4. **Pharmaceutical Companies**: Ensure compliance with safety standards

---

## 📚 References

- Material properties sourced from industry sustainability databases
- CO₂ calculations based on ISO 14067:2018 standards
- Recyclability ratings from EPA guidelines

---

**Last Updated**: January 12, 2026
**Version**: 2.0
**Author**: EcoPackAI Team
