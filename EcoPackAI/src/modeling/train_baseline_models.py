import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# --------------------------
# Paths
# --------------------------
DATA_PATH = "data/integrated_ecopack_dataset.csv"
PIPELINE_PATH = "ml/preprocessing/preprocessor.joblib"
METRICS_CSV_PATH = "ml/metrics/baseline_metrics.csv"

# --------------------------
# Load dataset
# --------------------------
print("📥 Loading dataset...")
df = pd.read_csv(DATA_PATH)

# Features & targets
feature_cols = [
    "product_category", "material_type", "product_weight", "fragility_score",
    "moisture_sensitivity", "thermal_sensitivity", "expected_shelf_life_days",
    "biodegradability_percent", "load_handling_score", "recyclability_category",
    "supplier_region", "hazardous_material_flag"
]
target_cost = "material_cost_per_kg"
target_co2 = "co2_emission_per_kg"

X_raw = df[feature_cols]
y_cost = df[target_cost]
y_co2 = df[target_co2]

# --------------------------
# Preprocessing
# --------------------------
print("📦 Creating preprocessing pipeline...")

categorical_cols = X_raw.select_dtypes(include=["object"]).columns.tolist()
numerical_cols = X_raw.select_dtypes(include=["int64", "float64"]).columns.tolist()

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=True), categorical_cols)
    ],
    remainder='drop'
)

X_processed = preprocessor.fit_transform(X_raw)

# Save preprocessor
os.makedirs(os.path.dirname(PIPELINE_PATH), exist_ok=True)
joblib.dump(preprocessor, PIPELINE_PATH)

# --------------------------
# Train/test split
# --------------------------
print("⚙️ Performing train/test split...")
X_train, X_test, y_cost_train, y_cost_test, y_co2_train, y_co2_test = train_test_split(
    X_processed, y_cost, y_co2, test_size=0.2, random_state=42
)

# --------------------------
# Train baseline models
# --------------------------
print("⚙️ Training baseline models...")

# Memory-safe: use SGDRegressor for cost prediction
cost_model = SGDRegressor(max_iter=1000, tol=1e-3, random_state=42)
cost_model.fit(X_train, y_cost_train)

# Decision Tree for CO2 (smaller memory footprint)
co2_model = DecisionTreeRegressor(random_state=42, max_depth=10)
co2_model.fit(X_train, y_co2_train)

# --------------------------
# Evaluate
# --------------------------
print("⚙️ Evaluating models...")

def compute_metrics(y_true, y_pred):
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "R2": r2_score(y_true, y_pred)
    }

y_cost_pred = cost_model.predict(X_test)
y_co2_pred = co2_model.predict(X_test)

metrics = []

metrics.append({
    "Model": "SGDRegressor",
    "Target": "Cost",
    **compute_metrics(y_cost_test, y_cost_pred)
})

metrics.append({
    "Model": "DecisionTreeRegressor",
    "Target": "CO2",
    **compute_metrics(y_co2_test, y_co2_pred)
})

# Save metrics
os.makedirs(os.path.dirname(METRICS_CSV_PATH), exist_ok=True)
pd.DataFrame(metrics).to_csv(METRICS_CSV_PATH, index=False)

print(f"📊 Metrics saved to {METRICS_CSV_PATH}")

# --------------------------
# Save models
# --------------------------
os.makedirs("ml/models", exist_ok=True)
joblib.dump(cost_model, "ml/models/cost_model.joblib")
joblib.dump(co2_model, "ml/models/co2_model.joblib")

print("✅ Baseline models trained and saved successfully!")
