import pandas as pd
import joblib

MODEL_PATH = "ml/models/xgb_co2_model.joblib"
X_PATH = "data/final/X_raw.csv"

# Load model
model = joblib.load(MODEL_PATH)

# Load features
X = pd.read_csv(X_PATH)

# Same preprocessing as training
X = pd.get_dummies(X, drop_first=True)
X = X.astype(float)

# Predict
preds = model.predict(X.head(5))

print("✅ Sample CO2 predictions:")
print(preds)
