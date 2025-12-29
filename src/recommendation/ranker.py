
import pandas as pd
import yaml

def rank_materials(df, config_path):
    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    w = cfg["weights"]
    c = cfg["constraints"]
    top_n = cfg["top_n"]

    def min_max(series, reverse=False):
        norm = (series - series.min()) / (series.max() - series.min())
        return 1 - norm if reverse else norm

    df = df.copy()
    df["cost_norm"] = min_max(df["predicted_cost"], reverse=True)
    df["co2_norm"] = min_max(df["predicted_co2"], reverse=True)
    df["suit_norm"] = min_max(df["Material_Suitability_Score"])

    df["ranking_score"] = (
        w["cost"] * df["cost_norm"] +
        w["co2"] * df["co2_norm"] +
        w["suitability"] * df["suit_norm"]
    )

    recy_map = {"A":4,"B":3,"C":2,"D":1}
    min_recy = recy_map[c["min_recyclability"]]

    df = df[
        (df["predicted_cost"] <= c["max_cost"]) &
        (df["Material_Suitability_Score"] >= c["min_suitability"]) &
        (df["Recyclability_Category"].map(recy_map) >= min_recy)
    ]

    df["rank"] = df.groupby("product_id")["ranking_score"]                    .rank(ascending=False, method="dense")

    return df[df["rank"] <= top_n].sort_values(["product_id","rank"])
