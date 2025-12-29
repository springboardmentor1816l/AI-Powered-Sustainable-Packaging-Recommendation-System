
# Material Ranking Logic

## Objective
Rank candidate packaging materials for each product using predicted cost,
predicted CO₂ impact, and Material Suitability Score.

## Ranking Criteria
- Cost (lower is better)
- CO₂ emissions (lower is better)
- Suitability score (higher is better)

All metrics are normalized to 0–1 before combining.

## Composite Score
score = w_cost * cost_norm +
        w_co2 * co2_norm +
        w_suitability * suit_norm

Weights are configurable via YAML.

## Constraints
Materials are filtered if:
- Recyclability below threshold
- Cost exceeds ceiling
- Suitability below minimum

## Output
Top-N ranked materials per product with ranks and scores.
