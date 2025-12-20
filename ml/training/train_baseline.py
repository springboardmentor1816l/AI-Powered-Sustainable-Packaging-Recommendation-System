
import pandas as pd
import joblib
import json
import os
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def train_and_track(version, description):
    X_path = "notebooks/data/final/X_raw.csv"
    y_path = "notebooks/data/final/y_raw.csv"
    
    if not os.path.exists(X_path):
        print(f"❌ Cannot find data at {X_path}")
        return

    X_train = pd.read_csv(X_path)
    y_train = pd.read_csv(y_path)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train.values.ravel())
    
    os.makedirs("ml/models/training", exist_ok=True)
    model_path = f"ml/models/training/packaging_model_{version}.pkl"
    joblib.dump(model, model_path)
    
    metrics = {"accuracy": float(accuracy_score(y_train, model.predict(X_train)))}
    metadata = {
        "experiment_id": version,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "model_type": "Random Forest Baseline",
        "metrics": metrics,
        "description": description
    }
    
    os.makedirs("ml/experiments/metadata", exist_ok=True)
    with open(f"ml/experiments/metadata/{version}_meta.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
    print(f"✅ SUCCESS: Model {version} and Metadata saved!")

if __name__ == "__main__":
    train_and_track("v1.0", "Baseline for EcoPackAI")
