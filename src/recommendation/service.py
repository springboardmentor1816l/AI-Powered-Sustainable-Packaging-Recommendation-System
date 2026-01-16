import pandas as pd

RANKED_PATH = "outputs/material_rankings.csv"

def get_ranked_recommendations(product_id, top_n=5):
    df = pd.read_csv(RANKED_PATH)

    df["product_id"] = df["product_id"].astype(int)

    # Filter product
    df = df[df["product_id"] == int(product_id)]

    if df.empty:
        return []

    # ✅ TAKE BEST ENTRY PER MATERIAL
    df = (
        df.sort_values("rank")
          .groupby("Material Type", as_index=False)
          .first()
    )

    # ✅ SORT AGAIN & LIMIT
    df = df.sort_values("rank").head(top_n)

    return df[[
        "Material Type",
        "predicted_cost",
        "predicted_co2",
        "final_score",
        "rank"
    ]].to_dict(orient="records")
