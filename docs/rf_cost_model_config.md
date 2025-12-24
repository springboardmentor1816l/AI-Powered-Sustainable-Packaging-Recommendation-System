# Random Forest Cost Prediction – Model Configuration

## Model Type
- Algorithm: Random Forest Regressor
- Task: Cost prediction (Regression)

---

## Hyperparameters

The following hyperparameters are selected for the baseline model:

- n_estimators: 200  
  Number of trees in the forest. A higher value improves stability.

- max_depth: 12  
  Controls tree depth to prevent overfitting.

- min_samples_split: 5  
  Minimum samples required to split an internal node.

- min_samples_leaf: 2  
  Minimum samples required at a leaf node.

- max_features: "sqrt"  
  Number of features considered for best split.

- bootstrap: True  
  Enables bootstrapping for variance reduction.

- random_state: 42  
  Ensures reproducibility.

---

## Training Strategy
- Model trained on training split only
- Cross-validation (5-fold) used for evaluation
- No test data exposure during training

---

## Performance Metrics
Primary evaluation metrics:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score

---

## Justification
Random Forest is chosen because:
- Handles non-linear relationships
- Robust to outliers
- Works well with mixed feature types
- Requires minimal feature scaling

---

## Conclusion
This configuration serves as a strong baseline for cost prediction and
can be tuned further in future experiments.
