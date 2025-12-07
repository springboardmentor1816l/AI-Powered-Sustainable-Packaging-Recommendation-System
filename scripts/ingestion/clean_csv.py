import pandas as pd
import os

RAW_DIR = "data/raw_datasets"
PROCESSED_DIR = "data/processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)

def clean_materials():
    df = pd.read_csv(f"{RAW_DIR}/materials_raw.csv")

    # convert column names to snake_case
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    df.to_csv(f"{PROCESSED_DIR}/materials_clean.csv", index=False)
    print("Created materials_clean.csv")

def clean_products():
    df = pd.read_csv(f"{RAW_DIR}/products_raw.csv")

    df.columns = df.columns.str.lower().str.replace(" ", "_")

    df.to_csv(f"{PROCESSED_DIR}/products_clean.csv", index=False)
    print("Created products_clean.csv")

def clean_sustainability():
    df = pd.read_csv(f"{RAW_DIR}/sustainability_raw.csv")

    df.columns = df.columns.str.lower().str.replace(" ", "_")

    df.to_csv(f"{PROCESSED_DIR}/sustainability_clean.csv", index=False)
    print("Created sustainability_clean.csv")

clean_materials()
clean_products()
clean_sustainability()

print("\nCleaning Completed!")
