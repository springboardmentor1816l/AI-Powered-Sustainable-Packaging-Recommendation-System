import pandas as pd
import os

RAW_DATA_PATH = "./data/raw_datasets/"

files = os.listdir(RAW_DATA_PATH)

for file in files:
    print("----------- Validating:", file, "-----------")
    file_path = os.path.join(RAW_DATA_PATH, file)
    df = pd.read_csv(file_path)

    print("\n[INFO]")
    print(df.info())

    print("\n[MISSING VALUES]")
    print(df.isnull().sum())

    print("\n[DUPLICATES]")
    print("Number of duplicate rows:", df.duplicated().sum())

    print("---------------------------------------------\n")
