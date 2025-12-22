
## 1. Objective

The goal of the preprocessing pipeline is to:
- Prepare an integrated Product × Material dataset for machine learning
- Handle missing values consistently
- Encode categorical variables safely
- Scale numeric features for model stability
- Ensure identical transformations during training and inference

---

## 2. Pipeline Architecture

The preprocessing pipeline is implemented using **scikit-learn's ColumnTransformer**.
Different transformations are applied to different feature groups.

Pipeline Components:
- Numeric Transformer
- Categorical Transformer
- ColumnTransformer wrapper

Excluded columns are explicitly dropped.

---

## 3. Numeric Feature Processing

### Transformations Applied
1. **Missing Value Imputation**
   - Strategy: `median`
   - Reason:
     - Robust to outliers
     - Suitable for skewed sustainability and cost metrics
     - Preserves realistic central tendencies

2. **Scaling**
   - Method: `StandardScaler`
   - Reason:
     - Normalizes features to mean = 0 and std = 1
     - Improves convergence of ML algorithms
     - Prevents dominance of large-scale features (e.g., cost, usage)

### Applied To
- Product weight and fragility
- Sustainability metrics
- Performance scores
- Cost and usage metrics

---

## 4. Categorical Feature Processing

### Transformations Applied
1. **Missing Value Handling**
   - Strategy: `most_frequent`
   - Reason:
     - Maintains valid category values
     - Prevents loss of rows

2. **Encoding**
   - Method: `OneHotEncoder`
   - Parameters:
     - `handle_unknown="ignore"`
     - `sparse_output=False`

### Reasoning
- One-hot encoding avoids introducing ordinal bias
- Ignoring unknown categories ensures robustness during inference
- Produces a stable and consistent feature space

---

## 5. Binary Feature Processing

- Currently not applicable
- If binary columns are introduced:
  - Values should be converted to numeric (0/1)
  - Missing values imputed using mode

---

## 6. ColumnTransformer Configuration

- Transformers:
  - Numeric → Imputation + Scaling
  - Categorical → Imputation + One-Hot Encoding
- `remainder="drop"`
  - Ensures excluded columns do not leak into the model
  - Prevents accidental inclusion of identifiers or text fields

---

## 7. Training & Inference Safety

- The pipeline is **fitted only on training data**
- Test and validation data are transformed using learned parameters
- Prevents data leakage
- Ensures reproducibility

---
