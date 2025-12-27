def passes_constraints(material, product):
    if material.get("recyclability_percent", 0) < 50:
        return False
    if product.get("fragility_index", 0) > material.get("fragility_support", 10):
        return False
    return True
