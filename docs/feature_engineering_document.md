# Feature Engineering Document – EcoPackAI

## 1. CO₂ Impact Index (CII)

### Objective
CO₂ Impact Index is designed to quantify the environmental sustainability
of a packaging material by combining carbon emissions, biodegradability,
and recyclability into a single standardized score.

The index helps compare materials on a uniform sustainability scale
and directly influences EcoPackAI’s recommendation ranking.

---

### Input Features
The following attributes are used to compute the CO₂ Impact Index:

- CO₂ Emission per kg of material
- Biodegradation Time (in days)
- Recyclability Category (A, B, C, D)
- Material Type (plastic, paper, metal, bio-based, etc.)

---

### Feature Transformation Logic (Conceptual)

1. **CO₂ Emissions Normalization**
   - Raw CO₂ emission values are normalized to a 0–1 scale.
   - Lower emissions receive a better (lower) impact score.

2. **Biodegradation Impact Score**
   - Biodegradation time is converted into an inverse green score.
   - Materials that degrade faster receive higher sustainability points.

3. **Recyclability Mapping**
   - Recyclability categories are mapped to numerical values:
     - A → 1.0 (Highly recyclable)
     - B → 0.75
     - C → 0.50
     - D → 0.25 (Poor recyclability)

4. **Material Type Weighting**
   - Bio-based and paper materials receive positive weighting.
   - Plastic and metal materials receive lower sustainability weighting.

5. **Weighted Aggregation**
   - All components are combined using predefined sustainability weights
     to compute a single environmental impact score.

---

### Output
- **CO₂ Impact Index (CII)**
- Value Range: **0–100**
- Higher score indicates better environmental sustainability.

---

### Usage
The CO₂ Impact Index is used by:
- Recommendation engine ranking
- Sustainability dashboards
- ML feature inputs for model training

## 2. Cost Efficiency Index (CEI)

### Objective
Cost Efficiency Index evaluates the economic feasibility of using a
packaging material by considering material cost, required packaging
weight, recyclability benefits, and durability.

This index ensures that EcoPackAI recommendations are not only
environmentally sustainable but also cost-effective.

---

### Input Features
The following attributes are used to compute the Cost Efficiency Index:

- Cost per kg of material
- Weight required for packaging a unit product
- Recyclability percentage or category
- Material durability / strength score

---

### Feature Transformation Logic (Conceptual)

1. **Cost Standardization**
   - Raw cost values are standardized to remove scale differences.
   - Lower cost materials receive higher efficiency scores.

2. **Cost per Unit Packaging**
   - Total packaging cost is estimated using:
     - Cost per kg × required packaging weight
   - Materials requiring less weight gain efficiency advantage.

3. **Recyclability Benefit Adjustment**
   - Recyclable or reusable materials receive a cost-efficiency boost.
   - Higher recyclability reduces long-term disposal and reuse costs.

4. **Durability Penalty**
   - Materials with low durability scores receive penalties.
   - High-cost but low-durability materials are deprioritized.

5. **Weighted Cost Aggregation**
   - All cost-related components are combined using predefined weights
     to generate a single cost efficiency score.

---

### Output
- **Cost Efficiency Index (CEI)**
- Value Range: **0–100**
- Higher score indicates better economic feasibility.

---

### Usage
The Cost Efficiency Index is used by:
- Cost-aware material ranking
- Budget-optimized packaging recommendations
- ML model features for price-performance tradeoff learning


## 3. Material Suitability Score (MSS)

### Objective
Material Suitability Score evaluates how appropriate a packaging material
is for a specific product category by matching material properties with
product handling and safety requirements.

This score ensures that recommended materials meet functional,
protective, and compliance needs of different product types.

---

### Input Features
The following attributes are used to compute the Material Suitability Score:

- Load handling / strength score
- Moisture resistance score
- Thermal resistance score
- Product category requirements (fragility, temperature sensitivity)
- Material durability rating
- Material type safety suitability (food-grade, pharma-safe, etc.)

---

### Feature Transformation Logic (Conceptual)

1. **Requirement Mapping**
   - Product category requirements are defined for:
     - Load capacity
     - Moisture protection
     - Thermal resistance
   - Each material’s attributes are mapped against these requirements.

2. **Mandatory Constraint Checks**
   - If a material fails a mandatory requirement
     (e.g., poor thermal resistance for heat-sensitive products),
     a strong penalty is applied.

3. **Attribute Matching Score**
   - Scores are assigned based on how closely material properties
     align with product needs.
   - Higher alignment results in higher suitability points.

4. **Bonus Adjustments**
   - Additional points are awarded for:
     - High durability
     - Proven safety compliance
     - Industry-specific suitability (e.g., food-grade materials)

5. **Weighted Aggregation**
   - All matching and penalty components are combined using
     predefined weights to compute a final suitability score.

---

### Output
- **Material Suitability Score (MSS)**
- Value Range: **0–100**
- Higher score indicates better suitability for the target product.

---

### Usage
The Material Suitability Score is used by:
- Product-specific material recommendations
- Risk-aware packaging selection
- ML models evaluating material–product compatibility
