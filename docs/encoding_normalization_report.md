# EcoPackAI — Encoding & Normalization Report
**Module:** Data Cleaning & Preprocessing

## Dataset Used
- Input: `cleaned_integrated_materials.csv`
- Output: `materials_final_encoded.csv`

---

## 1. Categorical Encoding

### Ordinal Encoding
Applied to:
- Material Type
- Packaging Type
- Supplier Region

Rationale:
These columns represent ordered or priority-based categorical attributes.
Ordinal encoding preserves this ordering while converting them into numeric form.

Encoder saved at:
- `models/encoders/ordinal_encoder.pkl`

---

### One-Hot Encoding (Single-label)
Applied to:
- Recyclability Category

Rationale:
This column represents nominal categories with no inherent ordering.
One-Hot Encoding prevents the model from assuming false ordinal relationships.

Encoder saved at:
- `models/encoders/onehot_encoder_recyclability.pkl`

---

### Multi-label One-Hot Encoding
Applied to:
- Suitable Product Categories
- Recommended Use Cases

Rationale:
These columns contain multiple categories per record (semicolon-separated).
Each unique category was converted into a separate binary feature to correctly
represent multi-label membership.

Delimiter used: `;`

Encoders saved at:
- `models/encoders/multilabel_encoder_products.pkl`
- `models/encoders/multilabel_encoder_usecases.pkl`

---

## 2. Numeric Normalization

The following normalization strategy (Option B) was applied:

| Column Type | Method |
|------------|--------|
| Percentages / bounded values | MinMaxScaler |
| Continuous metrics | StandardScaler |

Rationale:
- MinMaxScaler preserves relative proportions for bounded metrics.
- StandardScaler centers continuous variables to improve model convergence.

Scalers saved at:
- `models/scalers/numeric_scaler.pkl`

---

## 3. Post-processing Validation

The final encoded dataset was validated to ensure:

- No missing values are present
- All features are numeric
- All encoders and scalers are persisted for reuse
- Dataset is fully compatible with machine learning pipelines

---

## 4. Task Completion Status

- [x] Ordinal categorical features encoded
- [x] Nominal categorical features one-hot encoded
- [x] Multi-label categorical features handled correctly
- [x] Numeric features normalized
- [x] Encoders and scalers saved
- [x] Final dataset generated

