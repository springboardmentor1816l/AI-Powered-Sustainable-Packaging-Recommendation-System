import pandas as pd
import joblib

from .industry_preprocessor import preprocess_industry

# -----------------------------
# 1. Load trained XGBoost model
# -----------------------------
model = joblib.load("ml/xgboost_industry.pkl")
reference_columns = joblib.load("ml/xgb_reference_columns.pkl")

print("✅ XGBoost model loaded successfully")

# -----------------------------
# 2. Load dataset
# -----------------------------
df = pd.read_csv("data/integrated_dataset.csv")

TARGET = "sustainability_score"
y_true = df[TARGET]

# -----------------------------
# 3. Apply SAME industry preprocessing
# -----------------------------
X = preprocess_industry(df, reference_columns)

# -----------------------------
# 4. Take random samples for testing
# -----------------------------
sample = X.sample(5, random_state=42)
predictions = model.predict(sample)

# -----------------------------
# 5. Show results
# -----------------------------
print("\n🧪 XGBOOST MODEL TEST RESULTS\n")

for i, idx in enumerate(sample.index):
    print(f"Sample {i+1}")
    print("Predicted sustainability score:", round(predictions[i], 4))
    print("Actual sustainability score   :", round(y_true.loc[idx], 4))
    print("-" * 40)
