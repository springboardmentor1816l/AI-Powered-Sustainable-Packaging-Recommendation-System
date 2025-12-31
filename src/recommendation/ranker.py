import pandas as pd
import yaml
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler


class MaterialRanker:
    def __init__(self, config_path="config/ranking_weights.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.weights = self.config["weights"]
        self.constraints = self.config["constraints"]
        self.mode = self.config.get("mode", "balanced")

    def apply_constraints(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter out materials violating business constraints"""

        if "predicted_cost" in df.columns:
            df = df[df["predicted_cost"] <= self.constraints["max_cost"]]

        if "recyclability" in df.columns:
            df = df[df["recyclability"] >= self.constraints["min_recyclability"]]

        if "suitability_score" in df.columns:
            df = df[df["suitability_score"] >= self.constraints["min_suitability"]]

        return df

    def normalize_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize metrics to 0–1 scale"""

        scaler = MinMaxScaler()

        df[["cost_norm", "co2_norm"]] = scaler.fit_transform(
            df[["predicted_cost", "predicted_co2"]]
        )

        # Invert cost & CO2 (lower is better)
        df["cost_norm"] = 1 - df["cost_norm"]
        df["co2_norm"] = 1 - df["co2_norm"]

        return df

    def compute_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute final composite ranking score"""

        df["final_score"] = (
            self.weights["cost"] * df["cost_norm"]
            + self.weights["co2"] * df["co2_norm"]
            + self.weights["suitability"] * df["suitability_score"]
            + self.weights["sustainability"] * df["sustainability_score"]
        )

        return df

    def rank(self, df: pd.DataFrame, top_n=3) -> pd.DataFrame:
        """Rank materials per product"""

        df = self.apply_constraints(df)
        df = self.normalize_metrics(df)
        df = self.compute_score(df)

        df = df.sort_values(
            ["product_id", "final_score"], ascending=[True, False]
        )

        df["rank"] = df.groupby("product_id").cumcount() + 1

        return df[df["rank"] <= top_n]
