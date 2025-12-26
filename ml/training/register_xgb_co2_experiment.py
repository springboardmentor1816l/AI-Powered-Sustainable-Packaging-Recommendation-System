import json
import shutil
from pathlib import Path
from datetime import datetime
import pandas as pd

# -------------------------------------------------
# Paths
# -------------------------------------------------
EXP_ROOT = Path("../experiments")
EXP_ROOT.mkdir(parents=True, exist_ok=True)

MODEL_DIR = Path("../models")
METRIC_DIR = Path("../metrics")
REPORT_DIR = Path("../reports")

MODEL_FILE = "xgb_co2.joblib"
METRIC_FILE = "co2_metrics.csv"
FI_FILE = "feature_importance.csv"

EXP_ID = "co2_xgboost_v1_run1"

# -------------------------------------------------
# Create experiment directories
# -------------------------------------------------
exp_dir = EXP_ROOT / EXP_ID
art_dir = exp_dir / "artifacts"
art_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# Copy artifacts
# -------------------------------------------------
shutil.copy(MODEL_DIR / MODEL_FILE, art_dir / "model.pkl")
shutil.copy(METRIC_DIR / METRIC_FILE, art_dir / "metrics.csv")
shutil.copy(REPORT_DIR / FI_FILE, art_dir / "feature_importance.csv")

# -------------------------------------------------
# Metadata
# -------------------------------------------------
metadata = {
    "experiment_id": EXP_ID,
    "target": "co2",
    "model": "XGBoostRegressor",
    "dataset_version": "v1",
    "feature_set_version": "v1",
    "run_version": "run1",
    "created_at": datetime.utcnow().isoformat(),
    "random_seed": 42,
    "hyperparameters": {
        "objective": "reg:squarederror",
        "n_estimators": 200,
        "max_depth": 6,
        "learning_rate": 0.1,
        "subsample": 0.8,
        "colsample_bytree": 0.8
    },
    "preprocessing_pipeline": "models/preprocessing/preprocessing_pipeline.pkl",
    "data_inputs": {
        "X": "data/model_input/X_raw.csv",
        "Y": "data/model_input/Y_raw.csv",
        "target_column": "co2_emission_per_kg_estimated"
    },
    "evaluation": {
        "strategy": "80/20 Train-Test Split",
        "random_state": 42,
        "metrics": ["MAE", "RMSE", "R2"]
    },
    "notes": "XGBoost model trained for CO₂ prediction; used for explainability and downstream recommendation scoring"
}

with open(exp_dir / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

# -------------------------------------------------
# README
# -------------------------------------------------
with open(exp_dir / "README.md", "w", encoding="utf-8") as f:
    f.write(f"# {EXP_ID}\n\n")
    f.write("## Overview\n")
    f.write("XGBoost regression model for CO₂ emission prediction.\n\n")
    f.write("## Configuration\n")
    f.write("- Model: XGBoostRegressor\n")
    f.write("- Target: co2_emission_per_kg_estimated\n")
    f.write("- Dataset version: v1\n")
    f.write("- Feature set: v1\n")
    f.write("- Evaluation: 80/20 train-test split\n")
    f.write("- Random seed: 42\n")


print(f"Experiment '{EXP_ID}' registered successfully")
