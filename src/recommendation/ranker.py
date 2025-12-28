import pandas as pd
import yaml
import os

# ================= LOAD CONFIG =================
with open("config/ranking_weights.yaml", "r") as f:
    config = yaml.safe_load(f)

W = config["weights"]
C = config["constraints"]

# ================= NORMALIZATION =================
def min_max(series, reverse=False):
    norm = (series - series.min()) / (series.max() - series.min() + 1e-9)
    return 1 - norm if reverse else norm

# ================= RANKING FUNCTION =================
def rank_materials(df):
    # ---------- Apply Constraints ----------
    df = df[
        (df["predicted_cost"] <= C["max_cost"]) &
        (df["recyclability"] >= C["min_recyclability"]) &
        (df["suitability_score"] >= C["min_suitability"])
    ].copy()

    if df.empty:
        return df

    # ---------- Normalize ----------
    df["cost_norm"] = min_max(df["predicted_cost"], reverse=True)
    df["co2_norm"] = min_max(df["predicted_co2"], reverse=True)
    df["suitability_norm"] = min_max(df["suitability_score"])
    df["sustainability_norm"] = min_max(df["sustainability_score"])

    # ---------- Composite Score ----------
    df["final_score"] = (
        W["cost"] * df["cost_norm"] +
        W["co2"] * df["co2_norm"] +
        W["suitability"] * df["suitability_norm"] +
        W["sustainability"] * df["sustainability_norm"]
    )

    # ---------- Rank ----------
    df = df.sort_values(
        ["product_id", "final_score"],
        ascending=[True, False]
    )

    df["rank"] = df.groupby("product_id").cumcount() + 1
    return df
