import pandas as pd
import os

RAW_FOLDER = "data/raw_dataset/"
PROCESSED_FOLDER = "data/processed/"

def clean_file(filename):
    print(f"\n Validating file: {filename}")

    # Load CSV
    df = pd.read_csv(RAW_FOLDER + filename)

    # Print validation info
    print("\n--- BASIC INFO ---")
    print(df.info())
    print("\n--- NULL VALUES ---")
    print(df.isnull().sum())
    print("\n--- DUPLICATE ROWS ---")
    print(df.duplicated().sum())

    # Clean Column Names → snake_case
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Remove duplicates
    df = df.drop_duplicates()

    # Fill missing values with simple strategy
    df = df.fillna(method="ffill").fillna(method="bfill")

    # Export cleaned processed CSV
    output_path = PROCESSED_FOLDER + filename
    df.to_csv(output_path, index=False)

    print(f"CLEANED FILE SAVED → {output_path}")


def run_cleaning():
    files = ["material_dataset.csv", "product_dataset.csv"]

    print("Starting dataset validation + cleaning...")
    for f in files:
        clean_file(f)

    print("\n Cleaning complete! Processed files are ready.\n")


if __name__ == "__main__":
    run_cleaning()
