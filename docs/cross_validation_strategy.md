# Cross-Validation Strategy

We use 5-Fold Stratified Cross-Validation to ensure balanced
representation of material types in each fold.

- Method: StratifiedKFold
- Number of folds: 5
- Shuffle: Enabled
- Random Seed: 42

This strategy improves robustness and reduces evaluation bias.
