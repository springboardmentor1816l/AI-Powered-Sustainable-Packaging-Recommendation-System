# Cross-Validation Strategy

## Approach
- Stratified K-Fold Cross-Validation
- Number of folds: 5
- Stratification based on product_category
- Shuffling enabled to reduce ordering bias

## Rationale
Stratification ensures each fold maintains a representative distribution of product categories, preventing biased performance estimates in sustainability and cost prediction tasks.
