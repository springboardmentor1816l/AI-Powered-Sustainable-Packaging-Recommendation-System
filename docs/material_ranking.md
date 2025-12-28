
# Material Ranking Logic Documentation

## Optimization Goal
To recommend packaging materials that minimize environmental impact and cost while maximizing structural suitability.

## Scoring Formula
The engine uses a weighted composite score:
`Score = (0.4 * Norm_CO2) + (0.3 * Norm_Cost) + (0.3 * (1 - Norm_Suitability))`

## Hard Constraints Applied
1. **Load Capacity:** Material Load Handling Score must exceed Product Weight.
2. **Sustainability Floor:** Minimum recyclability threshold of 50.0%.
3. **Physical Protection:** Materials failing fragility compatibility are excluded.

## Ranking Configuration
| Criterion | Weight | Goal |
| :--- | :--- | :--- |
| CO2 Impact | 40.0% | Minimize |
| Cost Efficiency | 30.0% | Minimize |
| Suitability | 30.0% | Maximize |
