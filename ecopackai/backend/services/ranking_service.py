from services.inference import predict_sustainability
from recommendation.ranker import rank_materials
from recommendation.constraints import passes_constraints


def recommend_materials(request_payload):
    """
    Generate material recommendations based on sustainability prediction.
    """

    product = request_payload["product"]
    materials = request_payload["materials"]

    results = []

    for mat in materials:
        # Check hard constraints
        if not passes_constraints(mat, product):
            continue

        # Combine product + material info
        combined = {**product, **mat}

        # Predict sustainability score
        predicted_sustainability = predict_sustainability(combined)

        results.append({
            "material": mat["material_type"],
            "predicted_sustainability": predicted_sustainability,
            "suitability_score": mat.get("suitability_score", 70)
        })

    # Rank materials using weighted logic
    return rank_materials(results)


