import pandas as pd
from sklearn.model_selection import train_test_split
import os

# --------------------------------------------------
# LOAD FEATURE MATRIX AND TARGETS
# --------------------------------------------------
X = pd.read_csv("data/model_ready(2)/X_raw.csv")
y = pd.read_csv("data/model_ready(2)/y_raw.csv")

# --------------------------------------------------
# TRAIN / TEST SPLIT (80 / 20)
# --------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    shuffle=True
)

# --------------------------------------------------
# SAVE SPLITS
# --------------------------------------------------
os.makedirs("data/model_ready(2)", exist_ok=True)

X_train.to_parquet("data/model_ready(2)/X_train.parquet", index=False)
X_test.to_parquet("data/model_ready(2)/X_test.parquet", index=False)
y_train.to_parquet("data/model_ready(2)/y_train.parquet", index=False)
y_test.to_parquet("data/model_ready(2)/y_test.parquet", index=False)

print("Train-test split created successfully")
