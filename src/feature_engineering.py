def build_features(raw):

    features = {}

    # Derive engineering features
    features["recyclability_percent"] = 85 if raw["category"] in ["Food/Beverage", "Retail"] else 65
    features["biodegradability_percent"] = 70 if raw["category"] == "Food/Beverage" else 40
    features["strength_mpa"] = raw["fragility_index"] * 40 + 10
    features["weight_capacity"] = raw["product_weight"] * 1.5

    # Sustainability indices
    features["MSS"] = features["recyclability_percent"] * 0.4 + features["biodegradability_percent"] * 0.6
    features["CEI"] = raw["product_weight"] * 0.8
    features["CII"] = features["strength_mpa"] * 0.5

    # Material type (temporary logic)
    features["material_type_Cardboard"] = 1
    features["material_type_Paper/Bio-Based"] = 0
    features["material_type_Plastic"] = 0
    features["material_type_Steel"] = 0

    return features
