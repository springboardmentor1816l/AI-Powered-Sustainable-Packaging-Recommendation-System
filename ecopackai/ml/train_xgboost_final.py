import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from xgboost import XGBRegressor

from .industry_preprocessor import preprocess_industry

# -----------------------------
# 1. Load dataset
# -----------------------------
df = pd.read_csv("data/integrated_dataset.csv")
print("Dataset loaded:", df.shape)

TARGET = "sustainability_score"
y = df[TARGET]

# -----------------------------
# 2. Industry preprocessing (FIXED RULES)
# -----------------------------
X = preprocess_industry(df)

# Save schema (VERY IMPORTANT)
reference_columns = X.columns.tolist()

# -----------------------------
# 3. Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 4. Train XGBoost
# -----------------------------
xgb_model = XGBRegressor(
    n_estimators=300,        # epoch-like
    learning_rate=0.05,      # learning rate
    max_depth=8,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1
)

xgb_model.fit(X_train, y_train)

# -----------------------------
# 5. Evaluate
# -----------------------------
y_pred = xgb_model.predict(X_test)

print("\n🚀 XGBOOST (INDUSTRY FINAL)")
print("R² Score:", round(r2_score(y_test, y_pred), 4))
print("RMSE:", round(mean_squared_error(y_test, y_pred) ** 0.5, 4))

# -----------------------------
# 6. Save artifacts
# -----------------------------
joblib.dump(xgb_model, "ml/xgboost_industry.pkl")
joblib.dump(reference_columns, "ml/xgb_reference_columns.pkl")

print("\n✅ XGBoost industry model saved successfully")


