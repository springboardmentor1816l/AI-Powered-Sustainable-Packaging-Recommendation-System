import pandas as pd

df = pd.read_csv(
    "data/combined/combined_products_materials.csv"
)

def test_no_nulls():
    assert df.isnull().sum().sum() == 0

def test_score_ranges():
    for col in ["CII", "CEI", "MSS"]:
        assert ((df[col] >= 0) & (df[col] <= 100)).all()

