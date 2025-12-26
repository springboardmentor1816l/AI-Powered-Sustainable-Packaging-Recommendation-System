import pandas as pd
import joblib

# -----------------------------
# 1. Load trained Random Forest model
# -----------------------------
model = joblib.load("ml/random_forest_final.pkl")
print("✅ Random Forest model loaded successfully")

# -----------------------------
# 2. Load dataset
# -----------------------------
df = pd.read_csv("data/integrated_dataset.csv")

TARGET = "sustainability_score"

# -----------------------------
# 3. Remove leakage columns (same as training)
# -----------------------------
LEAKAGE_COLS = [
    "sustainability_score",
    "recyclability_percent",
    "co2_emission_score",
    "biodegradability_score",
    "sustainability_target_progress_percent"
]

X = df.drop(columns=[c for c in LEAKAGE_COLS if c in df.columns])
y_true = df[TARGET]

# -----------------------------
# 4. Encode categorical features
# -----------------------------
categorical_cols = X.select_dtypes(include=["object"]).columns
X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

# -----------------------------
# 5. Align features with training
# -----------------------------
X_encoded = X_encoded.reindex(
    columns=model.feature_names_in_,
    fill_value=0
)

# -----------------------------
# 6. Take random samples for testing
# -----------------------------
sample = X_encoded.sample(5, random_state=42)

# -----------------------------
# 7. Predict
# -----------------------------
predictions = model.predict(sample)

# -----------------------------
# 8. Show results
# -----------------------------
print("\n🧪 RANDOM FOREST MODEL TEST RESULTS\n")

for i, idx in enumerate(sample.index):
    print(f"Sample {i+1}")
    print("Predicted sustainability score:", round(predictions[i], 4))
    print("Actual sustainability score   :", round(y_true.loc[idx], 4))
    print("-" * 40)
