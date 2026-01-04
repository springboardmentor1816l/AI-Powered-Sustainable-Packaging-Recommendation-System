# Material Ranking Logic 

## Objective
The goal of this module is to rank sustainable packaging materials for each product
based on cost, CO2 emissions, material suitability, and recyclability.

This converts model predictions into actionable recommendations so that the
best material options appear at the top for each product.

## Ranking Criteria
The following metrics are used:

- Predicted Cost per unit (lower is better)
- Predicted CO2 emission (lower is better)
- Material Suitability Score (higher is better)
- Recyclability (higher is better)

## Normalization
Since cost and CO2 have different scales, they are normalized to 0–1.

normalized_value = (value − min) / (max − min)

## Composite Ranking Score
A weighted score is computed as:

final_score =
(cost_weight × normalized_cost) +
(co2_weight × normalized_co2) −
(suitability_weight × suitability_score) −
(recyclability_weight × recyclability)

Lower final_score = better rank.

## Ranking Modes
Three ranking strategies are supported:

1. Balanced Mode
   Equal emphasis on cost, CO2, suitability.

2. Sustainability First
   Higher priority to CO2 reduction.

3. Cost First
   Higher priority to lower cost.

## Constraints and Filters
Materials can be filtered based on:
- minimum recyclability threshold
- cost ceiling
- performance or strength limits

## Output
The system generates a ranked file:

- material_rankings.csv

which includes:
- product_id
- material_name
- final score
- rank
- cost
- CO2 emission
- suitability score
- recyclability score

## Validation Checklist
✔ Deterministic ranking results  
✔ Correct ordering per product  
✔ Configurable weights without code change  
✔ Business constraints applied correctly  
✔ Aligns with sustainability goals  

This completes the material ranking module documentation.
