# Train–Test Split Summary

## Dataset
Integrated Product × Material Dataset (EcoPackAI)

## Split Configuration
- Training Set: 80%
- Testing Set: 20%
- Random Seed: 42

## Stratification Criteria
The split preserves representative distributions across:
- Product categories (`category`)
- Packaging material types (`Material Type`)
- Shipping types (`shipping_type`)

A composite stratification strategy was used to avoid skewed splits
and maintain categorical balance.

## Leakage Prevention
- Product–material combinations are exclusive to each split
- Identifiers and descriptive text fields are excluded prior to splitting

## Distribution Validation
- Shipping Type:
  - Road ≈ 62%
  - Air ≈ 31%
  - Sea ≈ 7%
- Product and material category proportions remain consistent
  across training and testing datasets.

## Conclusion
The dataset split is balanced, leakage-free, and suitable for
robust model evaluation.
