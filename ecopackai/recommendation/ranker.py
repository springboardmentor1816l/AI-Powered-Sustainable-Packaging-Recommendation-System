import os
import yaml

# =====================================================
# Resolve path to weights.yaml safely
# =====================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # ecopackai/recommendation
WEIGHTS_PATH = os.path.join(BASE_DIR, "weights.yaml")

# =====================================================
# Load ranking weights
# =====================================================
with open(WEIGHTS_PATH, "r") as f:
    WEIGHTS = yaml.safe_load(f)


def compute_score(cost, co2, suitability):
    """
    Lower cost & CO2 are better
    Higher suitability is better
    """
    return (
        WEIGHTS["cost_weight"] * (1 / max(cost, 1e-6)) +
        WEIGHTS["co2_weight"] * (1 / max(co2, 1e-6)) +
        WEIGHTS["suitability_weight"] * (suitability / 100)
    )


def rank_materials(materials):
    """
    materials: list of dicts with keys:
    - predicted_cost
    - predicted_co2
    - suitability_score
    """

    for m in materials:
        m["final_score"] = compute_score(
            m["predicted_cost"],
            m["predicted_co2"],
            m["suitability_score"]
        )

    return sorted(materials, key=lambda x: x["final_score"], reverse=True)

