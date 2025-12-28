from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd
import joblib

# Load raw data
X_raw = pd.read_csv("data/final/X_raw.csv")
print("Columns in X_raw.csv:", X_raw.columns.tolist())

# Automatically select features
numeric_features = ['length', 'width', 'height', 'weight', 'fragility_enc']
categorical_features = [col for col in X_raw.select_dtypes(include=['object']).columns]

print("Numeric features:", numeric_features)
print("Categorical features:", categorical_features)

# Build preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ]
)

preprocessor.fit(X_raw)
joblib.dump(preprocessor, "models/preprocessing/preprocessor.joblib")
print("✅ Preprocessing pipeline saved at: models/preprocessing/preprocessor.joblib")
