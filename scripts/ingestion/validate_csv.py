import pandas as pd
import os

RAW_PATH = "data/raw_datasets/"
PROCESSED_PATH = "data/processed/"

files = {
    "materials": "material_dataset.csv",
    "products": "product_dataset.csv"
}

os.makedirs(PROCESSED_PATH, exist_ok=True)

for label, filename in files.items():
    file_path = os.path.join(RAW_PATH, filename)
    
    print(f"\n📌 Validating: {filename}")

    df = pd.read_csv(file_path)

    print(df.info())
    print("\nMissing Values:\n", df.isnull().sum())

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Remove duplicates
    df = df.drop_duplicates()

    # Save output
    output_path = os.path.join(PROCESSED_PATH, filename)
    df.to_csv(output_path, index=False)

    print(f"✔ Cleaned & saved to: {output_path}")
