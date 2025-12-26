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

MODEL_FILE = "rf_cost.joblib"
METRIC_FILE = "rf_cost_metrics.csv"

EXP_ID = "cost_random_forest_v1_run1"

# -------------------------------------------------
# Create experiment directories
# -------------------------------------------------
exp_dir = EXP_ROOT / EXP_ID
art_dir = exp_dir / "artifacts"
art_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# Copy model artifact
# -------------------------------------------------
shutil.copy(
    MODEL_DIR / MODEL_FILE,
    art_dir / "model.pkl"
)

# -------------------------------------------------
# Copy metrics
# -------------------------------------------------
metrics_df = pd.read_csv(METRIC_DIR / METRIC_FILE)
metrics_df.to_csv(art_dir / "metrics.csv", index=False)

# -------------------------------------------------
# Metadata
# -------------------------------------------------
metadata = {
    "experiment_id": EXP_ID,
    "target": "cost",
    "model": "RandomForestRegressor",
    "dataset_version": "v1",
    "feature_set_version": "v1",
    "run_version": "run1",
    "created_at": datetime.utcnow().isoformat(),
    "random_seed": 42,
    "hyperparameters": {
        "n_estimators": 200,
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "n_jobs": -1
    },
    "preprocessing_pipeline": "models/preprocessing/preprocessing_pipeline.pkl",
    "data_inputs": {
        "X": "data/model_input/X_raw.csv",
        "Y": "data/model_input/Y_raw.csv",
        "integration_reference": "data/integrated/integrated_dataset.csv"
    },
    "evaluation": {
        "strategy": "GroupKFold",
        "n_splits": 5,
        "group_by": "product_product_id",
        "metrics": ["MAE", "RMSE", "R2"]
    },
    "notes": "Random Forest baseline for cost prediction (no hyperparameter tuning)"
}

with open(exp_dir / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

# -------------------------------------------------
# README
# -------------------------------------------------
with open(exp_dir / "README.md", "w") as f:
    f.write(f"# {EXP_ID}\n\n")
    f.write("## Overview\n")
    f.write("Random Forest model trained for material cost prediction.\n\n")
    f.write("## Configuration\n")
    f.write("- Model: RandomForestRegressor\n")
    f.write("- Target: material_cost_per_unit_usd\n")
    f.write("- Dataset version: v1\n")
    f.write("- Feature set: v1\n")
    f.write("- CV: 5-fold GroupKFold\n")
    f.write("- Random seed: 42\n")

print(f"Experiment '{EXP_ID}' registered successfully")
