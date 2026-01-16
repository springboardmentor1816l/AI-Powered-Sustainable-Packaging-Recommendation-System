import pandas as pd
import itertools

RANKED_PATH = "outputs/material_rankings.csv"

_df = pd.read_csv(RANKED_PATH)
_product_ids = sorted(_df["product_id"].unique())

# Cycle through product_ids endlessly
_product_cycle = itertools.cycle(_product_ids)

def get_next_product_id():
    return int(next(_product_cycle))
