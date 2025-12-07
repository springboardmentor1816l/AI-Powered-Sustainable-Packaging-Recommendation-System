import pandas as pd
import os

RAW_DIR = "data/raw_datasets"

def validate_csv(file_name):
    path = os.path.join(RAW_DIR, file_name)
    print(f"\n--- Validating {file_name} ---")
    
    df = pd.read_csv(path)

    print("\nShape:", df.shape)
    print("\nColumns & Types:")
    print(df.info())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nSample Rows:")
    print(df.head())

files = ["materials_raw.csv", "products_raw.csv", "sustainability_raw.csv"]

for f in files:
    validate_csv(f)

print("\nValidation Completed!")
