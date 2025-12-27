from services.inference import predict_cost, predict_co2
from recommendation.ranker import rank_materials
from recommendation.constraints import passes_constraints

def recommend_materials(request_payload):
    product = request_payload["product"]
    materials = request_payload["materials"]

    results = []

    for mat in materials:
        combined_input = {**product, **mat}

        if not passes_constraints(mat, product):
            continue

        results.append({
            "material": mat["material_type"],
            "predicted_cost": predict_cost(combined_input),
            "predicted_co2": predict_co2(combined_input),
            "suitability_score": mat.get("suitability_score", 70)
        })

    return rank_materials(results)
