# Material Ranking Logic – EcoPackAI

## Objective
Rank packaging materials per product using predicted cost, CO₂ impact,
and suitability scores.

## Ranking Formula
Final Score =
w_cost × normalized_cost +
w_co2 × normalized_co2 +
w_suitability × (1 - normalized_suitability)

Lower score = better material.

## Constraints
- Recyclability ≥ 50%
- Load handling score ≥ 5

## Ranking Modes
- Sustainability-first
- Cost-first
- Balanced

## Output
Top-N ranked materials per product.
