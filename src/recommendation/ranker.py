import pandas as pd
import yaml

with open("config/ranking_weights.yaml") as f:
    cfg = yaml.safe_load(f)

def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

def rank_materials(df):
    df = df.copy()

    # Apply constraints (PDF aligned)
    df = df[df["recyclability_percent"] >= cfg["constraints"]["min_recyclability"]]
    df = df[df["cost_per_kg"] <= cfg["constraints"]["max_cost"]]

    # Normalize criteria (using real dataset fields)
    df["cost_n"] = normalize(df["cost_per_kg"])
    df["co2_n"] = normalize(df["co2_emission_score"])
    df["suitability_n"] = normalize(df["MSS"])

    w = cfg["weights"]

    # Composite score
    df["final_score"] = (
        w["cost"] * (1 - df["cost_n"]) +
        w["co2"] * (1 - df["co2_n"]) +
        w["suitability"] * df["suitability_n"]
    )

    # Rank materials per product
    df = df.sort_values(["product_id", "final_score"], ascending=[True, False])
    df["rank"] = df.groupby("product_id").cumcount() + 1

    return df
