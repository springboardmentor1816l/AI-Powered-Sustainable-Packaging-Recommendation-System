## Experiment Reproducibility

This document records all design choices and parameters required to
reproduce experiments reliably.

---

### Dataset Artifacts

- Features: `data/model_input/X_raw.csv`
- Targets: `data/model_input/Y_raw.csv`
- Integration reference: `data/integrated/integrated_dataset.csv`

Identifiers (`product_id`, `material_id`) are intentionally excluded
from model inputs and retained only for metadata-driven operations.

---

### Preprocessing

- Pipeline: `models/preprocessing/preprocessing_pipeline.pkl`
- Built using `ColumnTransformer`
- Targets and identifiers excluded
- Pipeline reused across all experiments

---

### Splitting & Validation

- **Train/Test Split**
  - Method: GroupShuffleSplit
  - Ratio: 80/20
  - Grouping: `product_id`
  - Random Seed: 42

- **Cross-Validation**
  - Strategy: GroupKFold
  - Folds: 5
  - Grouping: `product_id`

---

### Reproducibility Guarantees

- All randomness is controlled via fixed seeds
- Splits are index-based (no data duplication)
- Feature space is stable and identifier-free
- Group labels are externalized from model inputs

---

### Known Assumptions

- Products are the primary unit of generalization
- Materials may repeat across splits, products do not
- Targets are continuous (regression setting)
