## Cross-Validation Strategy

**Approach:** GroupKFold Cross-Validation  
**Number of Folds:** 5  
**Grouping Column:** `product_id`

---

### Why GroupKFold?

The dataset contains **multiple rows per product**, corresponding to
different material options.

Using standard K-Fold would allow the same product to appear in both
training and validation folds, causing **information leakage**.

GroupKFold ensures:
- Each product appears in **exactly one fold**
- Validation performance reflects **generalization to unseen products**
- No leakage across folds

---

### Implementation Details

- Group labels are extracted from `integrated_dataset.csv`
- `X_raw.csv` contains **features only**
- Group labels are never passed to preprocessing or models

---

### Outputs

For each fold `k`:
- `data/splits/cv_fold_k_train_idx.csv`
- `data/splits/cv_fold_k_val_idx.csv`

These indices can be reused across experiments to ensure
**consistent and comparable evaluations**.
