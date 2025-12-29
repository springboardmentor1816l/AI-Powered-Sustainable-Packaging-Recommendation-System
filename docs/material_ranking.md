# Material Ranking Logic – EcoPackAI

## Objective
To rank sustainable packaging materials for each product based on
predicted cost, CO₂ impact, material suitability, and recyclability.

## Ranking Criteria
- Predicted Cost (lower is better)
- Predicted CO₂ Emission (lower is better)
- Material Suitability Score (higher is better)
- Recyclability Percentage

## Scoring Method
All metrics are normalized using Min-Max scaling.
A weighted composite score is calculated.

## Ranking Formula
Final Score =
w_cost × (1 − cost_norm) +
w_co2 × (1 − co2_norm) +
w_suitability × suitability_norm +
w_recyclability × recyclability_norm

## Constraints Applied
- Minimum recyclability threshold
- Maximum allowed cost

## Output
Top-ranked materials are generated per product and saved as
material_rankings.csv.

## Conclusion
This ranking mechanism enables sustainability-aware and cost-effective
packaging recommendations.
