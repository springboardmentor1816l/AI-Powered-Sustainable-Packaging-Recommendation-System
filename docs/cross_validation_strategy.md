# Cross-Validation Strategy

## Method
- Stratified K-Fold Cross-Validation

## Configuration
- Number of folds: 5
- Shuffle: Enabled
- Random Seed: 42
- Stratification column: Material Type

## Rationale
- Maintains balanced class distribution across folds.
- Reduces variance in performance estimates.
- Prevents bias due to class imbalance.

## Usage
- Applied only on the training set.
- Test set remains untouched until final evaluation.
