# Cross-Validation Strategy

## Objective
To ensure reliable and unbiased model evaluation across diverse
product, material, and logistics scenarios.

## Method
Stratified K-Fold Cross-Validation

## Configuration
- Number of folds: 5
- Shuffle: Enabled
- Random Seed: 42

## Stratification Logic
Each fold maintains proportional representation of:
- Product categories
- Packaging material types
- Shipping types

## Rationale
Stratification reduces variance in performance estimates and ensures
that minority logistics scenarios (e.g., Sea shipping) are included
in every evaluation fold.
