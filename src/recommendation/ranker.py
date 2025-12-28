import pandas as pd
import yaml


def min_max_normalize(series, higher_is_better=True):
    if series.max() == series.min():
        return pd.Series([1.0] * len(series), index=series.index)

    if higher_is_better:
        return (series - series.min()) / (series.max() - series.min())
    else:
        return (series.max() - series) / (series.max() - series.min())


def apply_constraints(df, constraints):
    return df[
        (df["Recyclability (%)"] >= constraints["min_recyclability_percent"]) &
        (df["Load Handling Score"] >= constraints["min_load_handling_score"]) &
        (df["Moisture Resistance Score"] >= constraints["min_moisture_resistance_score"]) &
        (df["Thermal Resistance Score"] >= constraints["min_thermal_resistance_score"])
    ]


def compute_scores(df, weights):
    df = df.copy()

    df["cost_norm"] = min_max_normalize(
        df["predicted_cost"], higher_is_better=False
    )

    df["co2_norm"] = min_max_normalize(
        df["predicted_co2"], higher_is_better=False
    )

    df["suitability_norm"] = min_max_normalize(
        df["MSS"], higher_is_better=True
    )

    df["final_score"] = (
        weights["cost"] * df["cost_norm"] +
        weights["co2"] * df["co2_norm"] +
        weights["suitability"] * df["suitability_norm"]
    )

    return df


def rank_materials(
    data,
    ranking_mode,
    config_path="config/ranking_weights.yaml"
):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    weights = config["ranking_modes"][ranking_mode]["weights"]
    constraints = config["constraints"]
    top_n = config["output"]["top_n"]

    ranked_results = []

    for product_id, group in data.groupby("product_id"):
        valid_materials = apply_constraints(group, constraints)

        if valid_materials.empty:
            continue

        scored = compute_scores(valid_materials, weights)
        scored = scored.sort_values("final_score", ascending=False)
        scored["rank"] = range(1, len(scored) + 1)

        ranked_results.append(scored.head(top_n))

    return pd.concat(ranked_results, ignore_index=True)
