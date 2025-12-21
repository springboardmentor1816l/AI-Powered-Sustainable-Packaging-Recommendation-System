import os
import json
from datetime import datetime

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# =========================
# PATHS
# =========================
X_PATH = "data/final/X_regression_encoded_scaled.csv"
Y_PATH = "data/final/y_regression_raw.csv"

META_DIR = "ml/experiments/metadata"
MODEL_COST_DIR = "ml/models/cost"
MODEL_CO2_DIR = "ml/models/co2"
METRICS_PATH = "ml/metrics/baseline_metrics.csv"

os.makedirs(META_DIR, exist_ok=True)
os.makedirs(MODEL_COST_DIR, exist_ok=True)
os.makedirs(MODEL_CO2_DIR, exist_ok=True)


# =========================
# CONFIG
# =========================
RANDOM_SEED = 42
TEST_SIZE = 0.2
CV = KFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)

DATASET_VERSION = "integrated_v1"
FEATURE_VERSION = "regression_features_v1"


# =========================
# LOAD DATA
# =========================
print("🚀 Training baseline regression models")

X = pd.read_csv(X_PATH)
y = pd.read_csv(Y_PATH)

print("X shape:", X.shape)
print("y shape:", y.shape)


# =========================
# TARGETS & MODELS
# =========================
TARGETS = {
    "cost_per_unit_usd": MODEL_COST_DIR,
    "co2_emission_per_kg_estimated": MODEL_CO2_DIR
}

MODELS = {
    "LinearRegression": LinearRegression(),
    "DecisionTree": DecisionTreeRegressor(random_state=RANDOM_SEED)
}


# =========================
# TRAINING LOOP
# =========================
results = []
exp_id_counter = 1

for target, model_dir in TARGETS.items():

    y_target = y[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_target, test_size=TEST_SIZE, random_state=RANDOM_SEED
    )

    for model_name, model in MODELS.items():

        # Train
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_test)

        # Metrics
        mae = mean_absolute_error(y_test, y_pred)
        rmse = mean_squared_error(y_test, y_pred) ** 0.5
        r2 = r2_score(y_test, y_pred)

        cv_mae = -cross_val_score(
            model,
            X_train,
            y_train,
            scoring="neg_mean_absolute_error",
            cv=CV
        ).mean()

        # Save model
        model_path = os.path.join(model_dir, "model_v1.pkl")
        joblib.dump(model, model_path)

        # Experiment ID
        exp_id = f"exp_{exp_id_counter:03d}_{model_name.lower()}_{target}_v1"

        # Metadata
        metadata = {
            "experiment_id": exp_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dataset_version": DATASET_VERSION,
            "feature_set_version": FEATURE_VERSION,
            "model": {
                "type": model_name,
                "hyperparameters": model.get_params()
            },
            "target": target,
            "metrics": {
                "mae": mae,
                "rmse": rmse,
                "r2": r2,
                "cv_mae": cv_mae
            },
            "model_path": model_path
        }

        meta_path = os.path.join(META_DIR, f"{exp_id}.json")
        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=4)

        results.append({
            "experiment_id": exp_id,
            "model": model_name,
            "target": target,
            "mae": mae,
            "rmse": rmse,
            "r2": r2,
            "cv_mae": cv_mae
        })

        print(f"✅ Created experiment: {exp_id}")
        exp_id_counter += 1


# =========================
# SAVE METRICS
# =========================
pd.DataFrame(results).to_csv(METRICS_PATH, index=False)
print(f"📁 Metrics saved to {METRICS_PATH}")
