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

BASELINE_METRICS = pd.read_csv(METRIC_DIR / "baseline_metrics.csv")

# -------------------------------------------------
# Helper to create experiment
# -------------------------------------------------
def register_experiment(exp_id, target, model_name, model_file):
    exp_dir = EXP_ROOT / exp_id
    art_dir = exp_dir / "artifacts"
    art_dir.mkdir(parents=True, exist_ok=True)

    # Copy model
    shutil.copy(MODEL_DIR / model_file, art_dir / "model.pkl")

    # Filter and copy metrics
    metrics_subset = BASELINE_METRICS[BASELINE_METRICS["target"] == target]
    metrics_subset.to_csv(art_dir / "metrics.csv", index=False)

    # Metadata
    metadata = {
        "experiment_id": exp_id,
        "target": target,
        "model": model_name,
        "dataset_version": "v1",
        "feature_set_version": "v1",
        "run_version": "run1",
        "created_at": datetime.utcnow().isoformat(),
        "random_seed": 42,
        "preprocessing_pipeline": "models/preprocessing/preprocessing_pipeline.pkl",
        "evaluation": {
            "strategy": "GroupKFold",
            "n_splits": 5,
            "group_by": "product_product_id",
            "metrics": ["MAE", "RMSE", "R2"]
        },
        "notes": "Baseline experiment registered post-training"
    }

    with open(exp_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    # README
    with open(exp_dir / "README.md", "w") as f:
        f.write(f"# {exp_id}\n\n")
        f.write(f"- Target: {target}\n")
        f.write(f"- Model: {model_name}\n")
        f.write(f"- Dataset: v1\n")
        f.write(f"- Feature set: v1\n")
        f.write(f"- Run: run1\n")

    print(f"Registered {exp_id}")

# -------------------------------------------------
# Register baseline experiments
# -------------------------------------------------
register_experiment(
    exp_id="cost_linear_v1_run1",
    target="cost",
    model_name="LinearRegression",
    model_file="baseline_cost_model.pkl"
)

register_experiment(
    exp_id="co2_decision_tree_v1_run1",
    target="co2",
    model_name="DecisionTreeRegressor",
    model_file="baseline_co2_model.pkl"
)
