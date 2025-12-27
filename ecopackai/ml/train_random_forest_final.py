import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
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

X = df.drop(columns=[c for c in LEAKAGE_COLS if c in df.columns])
y = df[TARGET]

# -----------------------------
# 4. Identify feature types
# -----------------------------
numeric_features = X.select_dtypes(include=["int64", "float64"]).columns
categorical_features = X.select_dtypes(include=["object"]).columns

# -----------------------------
# 5. Preprocessing pipeline
# -----------------------------
numeric_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_pipeline, numeric_features),
        ("cat", categorical_pipeline, categorical_features)
    ]
)

# -----------------------------
# 6. Full RF pipeline
# -----------------------------
rf_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1
    ))
])

# -----------------------------
# 7. Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 8. Train
# -----------------------------
rf_pipeline.fit(X_train, y_train)

# -----------------------------
# 9. Evaluate
# -----------------------------
y_pred = rf_pipeline.predict(X_test)

r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5


print("\n🌳 Random Forest Final Results")
print("R² Score:", round(r2, 4))
print("RMSE:", round(rmse, 4))

# -----------------------------
# 10. Save pipeline (VERY IMPORTANT)
# -----------------------------
MODEL_PATH = "backend/models/rf_sustainability_pipeline.joblib"
os.makedirs("backend/models", exist_ok=True)

joblib.dump(rf_pipeline, MODEL_PATH)

print(f"\n✅ Random Forest pipeline saved at: {MODEL_PATH}")
