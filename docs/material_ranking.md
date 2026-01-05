# Material Ranking Logic – Week 16

This module ranks packaging materials for each product using predicted
cost, CO₂ emissions, and Material Suitability Score.

## Ranking Criteria
- Lower cost → higher rank
- Lower CO₂ → higher rank
- Higher suitability → higher rank

## Composite Score
Final Score = weighted sum of normalized metrics.

## Configurable Parameters
All weights and thresholds are defined in `config/ranking_weights.yaml`.

## Outputs
Ranked results stored in:
`outputs/material_rankings.csv`
