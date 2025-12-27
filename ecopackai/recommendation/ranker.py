import yaml

with open("recommendation/weights.yaml") as f:
    W = yaml.safe_load(f)

def compute_score(cost, co2, suitability):
    return (
        W["cost_weight"] * (1 / cost) +
        W["co2_weight"] * (1 / co2) +
        W["suitability_weight"] * (suitability / 100)
    )

def rank_materials(materials):
    for m in materials:
        m["final_score"] = compute_score(
            m["predicted_cost"],
            m["predicted_co2"],
            m["suitability_score"]
        )

    return sorted(materials, key=lambda x: x["final_score"], reverse=True)
