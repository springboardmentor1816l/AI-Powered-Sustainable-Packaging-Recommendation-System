import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

# -----------------------------
# 1. Load integrated dataset
# -----------------------------
df = pd.read_csv("data/integrated_dataset.csv")

print("Dataset shape:", df.shape)

# -----------------------------
# 2. Select target
# -----------------------------
TARGET = "sustainability_score"

# Drop rows where target is missing
df = df.dropna(subset=[TARGET])

# -----------------------------
# -----------------------------
# 3. Select numeric features (NO LEAKAGE)
# -----------------------------
LEAKAGE_COLS = [
    "sustainability_score",
    "biodegradability_score",
    "recyclability_percent",
    "co2_emission_score"
]

numeric_df = df.select_dtypes(include=[np.number])

X = numeric_df.drop(columns=[c for c in LEAKAGE_COLS if c in numeric_df.columns])
y = df["sustainability_score"]

print("Features used:", X.shape[1])


# -----------------------------
# 4. Train-test split (small check)
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# 5. LINEAR REGRESSION (baseline)
# -----------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lr = LinearRegression()
lr.fit(X_train_scaled, y_train)

y_pred_lr = lr.predict(X_test_scaled)

print("\n🔹 Linear Regression Results")
print("R² Score:", round(r2_score(y_test, y_pred_lr), 4))
rmse_lr = mean_squared_error(y_test, y_pred_lr) ** 0.5
print("RMSE:", round(rmse_lr, 4))


# -----------------------------
# 6. RANDOM FOREST (quick check)
# -----------------------------
rf = RandomForestRegressor(
    n_estimators=50,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

print("\n🔹 Random Forest Results")
print("R² Score:", round(r2_score(y_test, y_pred_rf), 4))
rmse_lr = mean_squared_error(y_test, y_pred_lr) ** 0.5
print("RMSE:", round(rmse_lr, 4))


print("\n Quick performance check completed")
