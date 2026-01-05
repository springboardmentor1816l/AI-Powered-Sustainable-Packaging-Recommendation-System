# Material Ranking Logic

## Objective
Rank sustainable packaging materials for each product using cost, CO₂ impact, and material suitability.

## Ranking Criteria
- Cost efficiency (lower cost preferred)
- Environmental impact (lower CO₂ preferred)
- Material suitability score

## Ranking Formula
Final Score =
w_cost × CostScore +
w_co2 × CO₂Score +
w_suitability × SuitabilityScore

## Constraints
- Minimum recyclability threshold
- Maximum cost limit

## Output
Top-ranked materials per product are generated in:
outputs/material_rankings.csv
