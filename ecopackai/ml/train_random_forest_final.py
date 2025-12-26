import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

# -----------------------------
# 1. Load dataset
# -----------------------------
df = pd.read_csv("data/integrated_dataset.csv")

print("Dataset loaded:", df.shape)

# -----------------------------
# 2. Define target
# -----------------------------
TARGET = "sustainability_score"

df = df.dropna(subset=[TARGET])

# -----------------------------
# 3. Remove leakage columns
# -----------------------------
LEAKAGE_COLS = [
    "sustainability_score",
    "biodegradability_score",
    "recyclability_percent",
    "co2_emission_score"
]

# -----------------------------
# 4. Encode categorical features
# -----------------------------
categorical_cols = df.select_dtypes(include=["object"]).columns

df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# -----------------------------
# 5. Prepare X and y
# -----------------------------
X = df_encoded.drop(columns=[c for c in LEAKAGE_COLS if c in df_encoded.columns])
y = df_encoded[TARGET]

print("Final feature count:", X.shape[1])

# -----------------------------
# 6. Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 7. Train Random Forest (FINAL)
# -----------------------------
rf_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)

# -----------------------------
# 8. Evaluate model
# -----------------------------
y_pred = rf_model.predict(X_test)

r2 = r2_score(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5

print("\n🌳 Random Forest Final Results")
print("R² Score:", round(r2, 4))
print("RMSE:", round(rmse, 4))

# -----------------------------
# 9. Save model
# -----------------------------
joblib.dump(rf_model, "ml/random_forest_final.pkl")

print("\n Random Forest model saved as random_forest_final.pkl")
