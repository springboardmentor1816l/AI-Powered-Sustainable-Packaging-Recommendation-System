from sklearn.ensemble import RandomForestRegressor
import joblib
import pandas as pd

def train(X, y, out_path="backend/models/model.joblib"):
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    joblib.dump(model, out_path)
    return out_path

def load_model(path="backend/models/model.joblib"):
    return joblib.load(path)
