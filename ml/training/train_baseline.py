
import pandas as pd
import joblib
import json
import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, mean_absolute_error

def run_auto_baseline(version):
    # 1. Load Data
    X = pd.read_csv("notebooks/data/final/X_raw.csv")
    y = pd.read_csv("notebooks/data/final/y_raw.csv")
    
    # We take the first column as the target (e.g., 'recommended_material')
    target_name = y.columns[0]
    y_target = y.iloc[:, 0]

    # 2. Split Data (Task 1: Dec 16th Module)
    X_train, X_test, y_train, y_test = train_test_split(X, y_target, test_size=0.2, random_state=42)

    # 3. Handle Data Type (Fixes the 'Cardboard' Error)
    if y_target.dtype == 'object':
        # If the data is text (like 'Cardboard'), use a Classifier
        print(f"📦 Target is text ({target_name}). Training a Classifier...")
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        score = accuracy_score(y_test, model.predict(X_test))
        metric_name = "accuracy"
    else:
        # If the data is numbers (like Cost), use a Regressor
        print(f"💰 Target is numeric ({target_name}). Training a Regressor...")
        model = LinearRegression()
        model.fit(X_train, y_train)
        score = mean_absolute_error(y_test, model.predict(X_test))
        metric_name = "mae"

    # 4. Save Metadata (Task 2: Tracking Doc)
    metadata = {
        "experiment_id": version,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "target": target_name,
        "metrics": {metric_name: float(score)}
    }
    
    os.makedirs("ml/experiments/metadata", exist_ok=True)
    with open(f"ml/experiments/metadata/{version}_meta.json", "w") as f:
        json.dump(metadata, f, indent=4)
    
    os.makedirs("ml/models/training", exist_ok=True)
    joblib.dump(model, f"ml/models/training/baseline_{version}.pkl")
    
    print(f"✅ Success! Experiment {version} finished with {metric_name}: {score:.2f}")

if __name__ == "__main__":
    run_auto_baseline("v1.2")