# Random Forest Cost Prediction - Training Summary
---

## 1️⃣ Feature & Target Selection

- **Features used (numeric only)**:  
  Product attributes: `product_weight_kg`, `fragility_index`, shipping type (encoded)  
  Material attributes: `Recyclability (%)`, `Recycled Content (%)`, `Reusability (%)`, `Biodegradation Time (days)`, `End-of-Life Disposal (%)`, `Carbon Footprint (kg CO2/unit)`, `CO2 Emission per kg (estimated)`, `Waste Reduction Impact (%)`, `Sustainability Target Progress (%)`, `Load Handling Score`, `Moisture Resistance Score`, `Thermal Resistance Score`, `Cost per Unit (USD)`, `Annual Usage (units)`, `Total Material Weight (tons)`, `Supplier Sustainability Compliance (%)`  
  Encoded categorical features: Packaging type, Material type, Recyclability category, Supplier region, Suitable product categories, Recommended packaging use cases.

- **Dropped non-numeric columns**: `product_name`, `Material ID`  
- **Target variable**: `Cost per Unit (USD)`

---

## 2️⃣ Model Configuration

- **Algorithm**: Random Forest Regressor  
- **Parameters**:
  - `n_estimators = 100`
  - `max_depth = None`
  - `random_state = 42`
  - `n_jobs = -1` (parallel processing)

- **Cross-validation**: 5-fold KFold, shuffled, `random_state = 42`

---

## 3️⃣ Training Process

- **Data split**: 80% training, 20% testing
- **Cross-validation** performed on training set
- **Training dataset**: `X_train` features, `y_train` target
- **Testing dataset**: `X_test` features, `y_test` target

---

## 4️⃣ Evaluation Metrics

| Metric | Value |
|--------|-------|
| CV Mean Absolute Error (MAE) | 5.65 × 10⁻¹⁵ |
| CV Root Mean Squared Error (RMSE) | 9.95 × 10⁻¹⁵ |
| Test MAE | 5.93 × 10⁻¹⁵ |
| Test RMSE | 9.55 × 10⁻¹⁵ |
| Test R² | 1.0 |

> ⚠️ Note: Extremely low error values indicate the model fits the dataset very closely. This may suggest **overfitting** if the dataset is small or lacks variability.

---

## 5️⃣ Model Persistence

- **Serialized model path**: `ml/models/rf_cost.joblib`
- **Metrics saved**: `ml/metrics/rf_cost_metrics.csv`
- **Reproducibility**: All features, target, and hyperparameters documented for future reference.

---
