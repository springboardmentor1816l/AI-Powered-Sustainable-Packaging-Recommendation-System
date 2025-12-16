import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# --------------------------------------------------
# 1. LOAD PRODUCTS DATASET
# --------------------------------------------------
df = pd.read_csv("data/raw(0)/products.csv")

# --------------------------------------------------
# 2. DEFINE COLUMNS (MATCHING YOUR CSV)
# --------------------------------------------------

numeric_features = [
    "product_weight",
    "fragility_index"
]

categorical_features = [
    "category",
    "shipping_type"
]

exclude_columns = [
    "product_id",
    "product_name"
]

X = df.drop(columns=exclude_columns)

# --------------------------------------------------
# 3. PIPELINES
# --------------------------------------------------

numeric_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

# --------------------------------------------------
# 4. COLUMN TRANSFORMER
# --------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_pipeline, numeric_features),
        ("cat", categorical_pipeline, categorical_features)
    ]
)

# --------------------------------------------------
# 5. FIT & TRANSFORM
# --------------------------------------------------

X_transformed = preprocessor.fit_transform(X)

# --------------------------------------------------
# 6. SAVE PIPELINE
# --------------------------------------------------

joblib.dump(
    preprocessor,
    "Scripts/preprocessing/preprocessing_pipeline.pkl"
)

# --------------------------------------------------
# 7. SAVE SAMPLE TRANSFORMED OUTPUT
# --------------------------------------------------

pd.DataFrame(X_transformed[:50]).to_csv(
    "data/model_ready(2)/sample_transformed.csv",
    index=False
)

print("Preprocessing pipeline built successfully for products dataset")
