import pandas as pd
import joblib
import os

from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# ================= PATHS =================
X_PATH = "data/final/X_raw.csv"
Y_PATH = "data/final/y_co2.csv"
MODEL_PATH = "ml/models/xgb_co2_model.joblib"

# ================= LOAD DATA =================
X = pd.read_csv(X_PATH)
y = pd.read_csv(Y_PATH).iloc[:, 0]   # convert dataframe to series

print("Loaded shapes:", X.shape, y.shape)

# ================= PREPROCESS =================
# Convert categorical columns to numeric
X = pd.get_dummies(X, drop_first=True)

# Ensure everything is numeric
X = X.astype(float)

# Safety check
assert not y.isna().any(), "❌ y contains NaN values"

# ================= TRAIN-TEST SPLIT =================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ================= MODEL =================
model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

# ================= EVALUATION =================
y_pred = model.predict(X_test)

print("MAE:", mean_absolute_error(y_test, y_pred))
print("R2 :", r2_score(y_test, y_pred))

# ================= SAVE MODEL =================
os.makedirs("ml/models", exist_ok=True)
joblib.dump(model, MODEL_PATH)

print("✅ CO2 model saved at:", MODEL_PATH)
