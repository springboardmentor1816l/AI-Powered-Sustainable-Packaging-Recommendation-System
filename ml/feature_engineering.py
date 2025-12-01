import pandas as pd
import numpy as np

def load_raw(path: str):
    return pd.read_csv(path)

def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    # placeholder cleaning
    df = df.dropna(subset=["material","cost","co2_kg"])
    return df

def compute_sustainability_score(df: pd.DataFrame) -> pd.DataFrame:
    # example engineered metric
    df["sustainability_score"] = 1 / (1 + df["co2_kg"])  # simple inverse
    return df
