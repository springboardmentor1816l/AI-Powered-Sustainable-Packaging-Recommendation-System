import pandas as pd

class MaterialRanker:
    def __init__(self, mode="balanced"):
        # Weight configurations for different ranking strategies
        modes = {
            "balanced": dict(cost=0.3, co2=0.3, suit=0.3, recycle=0.1),
            "sustainability_first": dict(cost=0.2, co2=0.45, suit=0.25, recycle=0.1),
            "cost_first": dict(cost=0.5, co2=0.2, suit=0.2, recycle=0.1),
        }

        self.weights = modes[mode]

    # Normalization function (to scale values between 0 and 1)
    def normalize(self, series):
        return (series - series.min()) / (series.max() - series.min() + 1e-9)

    # Ranking Logic
    def rank(self, df):
        # Normalize cost & CO2
        df["norm_cost"] = self.normalize(df["predicted_cost"])
        df["norm_co2"] = self.normalize(df["predicted_co2"])

        # Final composite ranking score
        df["final_score"] = (
            df["norm_cost"] * self.weights["cost"] +
            df["norm_co2"] * self.weights["co2"] -
            df["suitability_score"] * self.weights["suit"] -
            df["recyclability"] * self.weights["recycle"]
        )

        # Rank per product (lower score = better)
        df["rank"] = (
            df.groupby("product_id")["final_score"]
            .rank(method="dense", ascending=True)
        )

        # Sort final output
        df = df.sort_values(["product_id", "final_score"])
        return df

