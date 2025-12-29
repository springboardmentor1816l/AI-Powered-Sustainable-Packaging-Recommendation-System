import pandas as pd
import numpy as np
import yaml
from pathlib import Path

# -------------------------------------------------
# Helpers
# -------------------------------------------------
def minmax(series, invert=False):
    s = (series - series.min()) / (series.max() - series.min() + 1e-9)
    return 1 - s if invert else s

def compute_suitability(df):
    load = minmax(df["load_handling_score"])
    moist = minmax(df["moisture_resistance_score"])
    therm = minmax(df["thermal_resistance_score"])

    # fragility_index: 1 (low fragility) → best, 5 (high fragility) → worst
    frag_compat = 1 - (df["fragility_index"] - 1) / 4.0
    frag_compat = frag_compat.clip(0, 1)

    return (load + moist + therm + frag_compat) / 4.0

# -------------------------------------------------
# Ranker
# -------------------------------------------------
class MaterialRanker:
    def __init__(self, config_path: Path):
        with open(config_path, "r", encoding="utf-8") as f:
            self.cfg = yaml.safe_load(f)

    def apply_constraints(self, df):
        c = self.cfg["constraints"]

        df = df[df["recyclability_"] >= c["min_recyclability_percent"]]
        df = df[df["supplier_sustainability_compliance_"] >= c["min_supplier_compliance_percent"]]

        cost_cap = df["predicted_cost"].quantile(c["max_cost_percentile"] / 100)
        df = df[df["predicted_cost"] <= cost_cap]
        return df

    def rank(self, df: pd.DataFrame, mode: str) -> pd.DataFrame:
        w = self.cfg["modes"][mode]["weights"]

        # Compute suitability
        df = df.copy()
        df["suitability_score"] = compute_suitability(df)

        # Normalize metrics PER PRODUCT
        ranked = []
        for pid, g in df.groupby("product_id"):
            g = self.apply_constraints(g)

            g["n_cost"] = minmax(g["predicted_cost"], invert=True)
            g["n_co2"] = minmax(g["predicted_co2"], invert=True)
            g["n_suit"] = minmax(g["suitability_score"])
            g["n_comp"] = minmax(g["supplier_sustainability_compliance_"])

            g["final_score"] = (
                w["cost"] * g["n_cost"]
                + w["co2"] * g["n_co2"]
                + w["suitability"] * g["n_suit"]
                + w["compliance"] * g["n_comp"]
            )

            g = g.sort_values("final_score", ascending=False)
            g["rank"] = np.arange(1, len(g) + 1)
            ranked.append(g)

        return pd.concat(ranked, ignore_index=True)

# -------------------------------------------------
# Runner
# -------------------------------------------------
if __name__ == "__main__":
    DATA_PATH = Path("../../data/integrated/integrated_with_predictions.csv")
    CFG_PATH = Path("../../config/ranking_weights.yaml")
    OUT_PATH = Path("../../outputs/material_rankings.csv")
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    # Expected columns:
    # product_id, material_id
    # predicted_cost, predicted_co2
    # load_handling_score, moisture_resistance_score, thermal_resistance_score, fragility_index
    # recyclability_percent, supplier_sustainability_compliance_percent

    ranker = MaterialRanker(CFG_PATH)
    result = ranker.rank(df, mode="balanced")

    keep = [
        "product_id", "material_id", "rank", "final_score",
        "predicted_cost", "predicted_co2",
        "suitability_score", "supplier_sustainability_compliance_"
    ]
    result[keep].to_csv(OUT_PATH, index=False)
    print("Material rankings generated:", OUT_PATH)
