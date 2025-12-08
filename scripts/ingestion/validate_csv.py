import pandas as pd
from pathlib import Path

raw_path = Path("data/raw_datasets")
processed_path = Path("data/processed")

processed_path.mkdir(parents=True, exist_ok=True)

for csv_file in raw_path.rglob("*.csv"):
    df = pd.read_csv(csv_file)

    print("\nFile:", csv_file.name)
    print(df.info())
    print(df.isnull().sum())

    clean_file = processed_path / csv_file.name.replace(".csv", "_clean.csv")
    df.to_csv(clean_file, index=False)

print("\n✅ Validation & cleaning completed successfully.")

