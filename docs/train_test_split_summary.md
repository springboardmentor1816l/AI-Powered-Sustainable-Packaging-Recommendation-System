## Train/Test Split Summary

**Objective:**  
Create a leakage-free, reproducible train/test split for a relational
(Product × Material) dataset.

---

### Split Configuration

- **Method:** Group-aware split
- **Split Ratio:** 80% Train / 20% Test
- **Grouping Column:** `product_id`
- **Random Seed:** 42

---

### Design Rationale

Each row in the dataset represents a **product–material pairing**.
If the same product appears in both training and test sets, the model
would indirectly see the same product requirements during evaluation,
resulting in **data leakage**.

To prevent this:
- `product_id` is used **only for grouping**
- Identifiers are **explicitly excluded from X_raw**
- Group labels are sourced from `integrated_dataset.csv`

This ensures that:
- The model is evaluated on **entirely unseen products**
- Feature space remains free of identifiers

---

### Outputs

- `data/splits/train_indices.csv`
- `data/splits/test_indices.csv`
- `ml/metadata/split_metadata.json`

Indices reference row positions in `X_raw.csv` and `Y_raw.csv`.

---

### Leakage Prevention Guarantee

- No identifiers are present in model inputs
- Grouping is performed externally using metadata
- Train/test separation is strictly enforced at the product level
