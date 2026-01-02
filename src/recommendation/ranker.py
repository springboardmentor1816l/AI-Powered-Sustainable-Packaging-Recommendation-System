"""
Material Ranking Module
=======================

This module implements the core material ranking logic for sustainable packaging
recommendation. It evaluates and ranks materials based on multiple criteria including
cost, CO₂ emissions, material suitability, and sustainability compliance.

Author: EcoPackAI Team
Date: 2026-01-02
"""

import pandas as pd
import numpy as np
import yaml
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass, asdict
import warnings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RankingConfig:
    """Configuration for material ranking"""
    ranking_mode: str
    weights: Dict[str, float]
    constraints: Dict[str, float]
    normalization_method: str
    top_n: int
    include_explanations: bool
    enable_sustainability_bonus: bool
    bonus_threshold: float
    bonus_multiplier: float


class MaterialRanker:
    """
    Material Ranking System for Sustainable Packaging Recommendation
    
    This class implements a multi-criteria ranking system that evaluates
    packaging materials based on environmental impact, cost, suitability,
    and sustainability compliance.
    
    Attributes:
        config (RankingConfig): Ranking configuration
        ranking_mode (str): Current ranking mode (sustainability_first, cost_first, balanced)
        weights (dict): Criterion weights for current mode
        constraints (dict): Business constraints for filtering
    """
    
    def __init__(self, config_path: Optional[str] = None, ranking_mode: str = "balanced"):
        """
        Initialize the Material Ranker
        
        Args:
            config_path: Path to YAML configuration file
            ranking_mode: Ranking mode to use (overrides config)
        """
        self.config_path = config_path
        self.ranking_mode = ranking_mode
        
        # Load configuration
        if config_path and Path(config_path).exists():
            self._load_config(config_path)
        else:
            logger.warning(f"Config file not found: {config_path}. Using default configuration.")
            self._load_default_config()
        
        # Override with specified ranking mode
        if ranking_mode in self.config_weights:
            self.weights = self.config_weights[ranking_mode]
            logger.info(f"Loaded ranking mode: {ranking_mode}")
        else:
            logger.warning(f"Invalid ranking mode: {ranking_mode}. Using balanced mode.")
            self.weights = self.config_weights.get('balanced', self._get_default_weights())
        
        # Validate configuration
        self._validate_config()
        
        logger.info("MaterialRanker initialized successfully")
    
    def _load_config(self, config_path: str):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            self.config_weights = config.get('weights', {})
            self.constraints = config.get('constraints', {})
            self.normalization_config = config.get('normalization', {})
            self.output_config = config.get('output', {})
            self.advanced_config = config.get('advanced', {})
            
            logger.info(f"Configuration loaded from {config_path}")
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self._load_default_config()
    
    def _load_default_config(self):
        """Load default configuration"""
        self.config_weights = {
            'balanced': self._get_default_weights()
        }
        self.constraints = self._get_default_constraints()
        self.normalization_config = {'method': 'min_max'}
        self.output_config = {'top_n_recommendations': 5, 'include_explanations': True}
        self.advanced_config = {'sustainability_bonus': {'enabled': True, 'recyclability_threshold': 80.0, 'bonus_multiplier': 1.1}}
    
    def _get_default_weights(self) -> Dict[str, float]:
        """Get default balanced weights"""
        return {
            'co2_emission': 0.30,
            'cost': 0.30,
            'material_suitability': 0.25,
            'recyclability': 0.10,
            'sustainability_compliance': 0.05
        }
    
    def _get_default_constraints(self) -> Dict[str, float]:
        """Get default constraints"""
        return {
            'min_recyclability_percent': 30.0,
            'max_cost_per_unit': 100.0,
            'min_load_handling_score': 40.0,
            'min_moisture_resistance_score': 30.0,
            'min_thermal_resistance_score': 30.0,
            'min_material_suitability_score': 40.0,
            'min_sustainability_compliance_percent': 50.0
        }
    
    def _validate_config(self):
        """Validate configuration weights sum to 1.0"""
        total_weight = sum(self.weights.values())
        if not np.isclose(total_weight, 1.0, atol=0.01):
            logger.warning(f"Weights sum to {total_weight}, not 1.0. Normalizing...")
            self.weights = {k: v/total_weight for k, v in self.weights.items()}
    
    def apply_constraints(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply business constraints to filter out invalid materials
        
        Args:
            df: DataFrame with material features
            
        Returns:
            Filtered DataFrame with only valid materials
        """
        initial_count = len(df)
        df_filtered = df.copy()
        
        # Track which materials are filtered and why
        filter_reasons = []
        
        # Apply recyclability constraint
        if 'min_recyclability_percent' in self.constraints:
            min_rec = self.constraints['min_recyclability_percent']
            mask = df_filtered['recyclability_percent'] >= min_rec
            filtered_count = (~mask).sum()
            if filtered_count > 0:
                filter_reasons.append(f"Recyclability < {min_rec}%: {filtered_count} materials")
            df_filtered = df_filtered[mask]
        
        # Apply cost constraint
        if 'max_cost_per_unit' in self.constraints:
            max_cost = self.constraints['max_cost_per_unit']
            if 'predicted_cost' in df_filtered.columns:
                mask = df_filtered['predicted_cost'] <= max_cost
            elif 'cost_per_unit_usd' in df_filtered.columns:
                mask = df_filtered['cost_per_unit_usd'] <= max_cost
            else:
                mask = pd.Series([True] * len(df_filtered))
            
            filtered_count = (~mask).sum()
            if filtered_count > 0:
                filter_reasons.append(f"Cost > ${max_cost}: {filtered_count} materials")
            df_filtered = df_filtered[mask]
        
        # Apply load handling constraint
        if 'min_load_handling_score' in self.constraints:
            min_load = self.constraints['min_load_handling_score']
            if 'load_handling_score' in df_filtered.columns:
                mask = df_filtered['load_handling_score'] >= min_load
                filtered_count = (~mask).sum()
                if filtered_count > 0:
                    filter_reasons.append(f"Load handling < {min_load}: {filtered_count} materials")
                df_filtered = df_filtered[mask]
        
        # Apply moisture resistance constraint
        if 'min_moisture_resistance_score' in self.constraints:
            min_moisture = self.constraints['min_moisture_resistance_score']
            if 'moisture_resistance_score' in df_filtered.columns:
                mask = df_filtered['moisture_resistance_score'] >= min_moisture
                filtered_count = (~mask).sum()
                if filtered_count > 0:
                    filter_reasons.append(f"Moisture resistance < {min_moisture}: {filtered_count} materials")
                df_filtered = df_filtered[mask]
        
        # Apply thermal resistance constraint
        if 'min_thermal_resistance_score' in self.constraints:
            min_thermal = self.constraints['min_thermal_resistance_score']
            if 'thermal_resistance_score' in df_filtered.columns:
                mask = df_filtered['thermal_resistance_score'] >= min_thermal
                filtered_count = (~mask).sum()
                if filtered_count > 0:
                    filter_reasons.append(f"Thermal resistance < {min_thermal}: {filtered_count} materials")
                df_filtered = df_filtered[mask]
        
        # Apply material suitability constraint
        if 'min_material_suitability_score' in self.constraints:
            min_suit = self.constraints['min_material_suitability_score']
            if 'material_suitability_score' in df_filtered.columns:
                mask = df_filtered['material_suitability_score'] >= min_suit
                filtered_count = (~mask).sum()
                if filtered_count > 0:
                    filter_reasons.append(f"Suitability < {min_suit}: {filtered_count} materials")
                df_filtered = df_filtered[mask]
        
        # Apply sustainability compliance constraint
        if 'min_sustainability_compliance_percent' in self.constraints:
            min_compliance = self.constraints['min_sustainability_compliance_percent']
            if 'supplier_sustainability_compliance_percent' in df_filtered.columns:
                mask = df_filtered['supplier_sustainability_compliance_percent'] >= min_compliance
                filtered_count = (~mask).sum()
                if filtered_count > 0:
                    filter_reasons.append(f"Compliance < {min_compliance}%: {filtered_count} materials")
                df_filtered = df_filtered[mask]
        
        final_count = len(df_filtered)
        filtered_total = initial_count - final_count
        
        logger.info(f"Constraint filtering: {initial_count} → {final_count} materials ({filtered_total} filtered)")
        if filter_reasons:
            for reason in filter_reasons:
                logger.info(f"  - {reason}")
        
        return df_filtered
    
    def normalize_features(self, df: pd.DataFrame, features: List[str]) -> pd.DataFrame:
        """
        Normalize features to comparable scales
        
        Args:
            df: DataFrame with features
            features: List of feature names to normalize
            
        Returns:
            DataFrame with normalized features
        """
        df_norm = df.copy()
        method = self.normalization_config.get('method', 'min_max')
        
        for feature in features:
            if feature not in df_norm.columns:
                logger.warning(f"Feature {feature} not found in DataFrame")
                continue
            
            if method == 'min_max':
                # Min-max normalization to [0, 1]
                min_val = df_norm[feature].min()
                max_val = df_norm[feature].max()
                
                if max_val - min_val > 0:
                    df_norm[f'{feature}_norm'] = (df_norm[feature] - min_val) / (max_val - min_val)
                else:
                    df_norm[f'{feature}_norm'] = 0.5  # All values are the same
                    
            elif method == 'z_score':
                # Z-score normalization
                mean_val = df_norm[feature].mean()
                std_val = df_norm[feature].std()
                
                if std_val > 0:
                    df_norm[f'{feature}_norm'] = (df_norm[feature] - mean_val) / std_val
                    # Clip to reasonable range and rescale to [0, 1]
                    df_norm[f'{feature}_norm'] = df_norm[f'{feature}_norm'].clip(-3, 3)
                    df_norm[f'{feature}_norm'] = (df_norm[f'{feature}_norm'] + 3) / 6
                else:
                    df_norm[f'{feature}_norm'] = 0.5
                    
            elif method == 'robust':
                # Robust normalization using median and IQR
                median_val = df_norm[feature].median()
                q1 = df_norm[feature].quantile(0.25)
                q3 = df_norm[feature].quantile(0.75)
                iqr = q3 - q1
                
                if iqr > 0:
                    df_norm[f'{feature}_norm'] = (df_norm[feature] - median_val) / iqr
                    # Clip and rescale
                    df_norm[f'{feature}_norm'] = df_norm[f'{feature}_norm'].clip(-2, 2)
                    df_norm[f'{feature}_norm'] = (df_norm[f'{feature}_norm'] + 2) / 4
                else:
                    df_norm[f'{feature}_norm'] = 0.5
        
        return df_norm
    
    def calculate_ranking_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate composite ranking score for each material
        
        Args:
            df: DataFrame with normalized features
            
        Returns:
            DataFrame with ranking scores added
        """
        df_scored = df.copy()
        
        # Initialize score
        df_scored['ranking_score'] = 0.0
        df_scored['score_breakdown'] = ''
        
        # Map feature names to normalized columns
        feature_mapping = {
            'co2_emission': 'predicted_co2' if 'predicted_co2' in df.columns else 'co2_emission_per_kg_estimated',
            'cost': 'predicted_cost' if 'predicted_cost' in df.columns else 'cost_per_unit_usd',
            'material_suitability': 'material_suitability_score',
            'recyclability': 'recyclability_percent',
            'sustainability_compliance': 'supplier_sustainability_compliance_percent'
        }
        
        # Normalize all relevant features
        features_to_normalize = [v for v in feature_mapping.values() if v in df.columns]
        df_scored = self.normalize_features(df_scored, features_to_normalize)
        
        # Calculate weighted score
        breakdown_parts = []
        
        for criterion, weight in self.weights.items():
            if criterion not in feature_mapping:
                continue
            
            feature_name = feature_mapping[criterion]
            norm_feature = f'{feature_name}_norm'
            
            if norm_feature not in df_scored.columns:
                logger.warning(f"Normalized feature {norm_feature} not found")
                continue
            
            # For cost and CO2, lower is better, so we invert the normalized score
            if criterion in ['co2_emission', 'cost']:
                contribution = weight * (1 - df_scored[norm_feature])
            else:
                # For other metrics, higher is better
                contribution = weight * df_scored[norm_feature]
            
            df_scored['ranking_score'] += contribution
            
            # Track breakdown
            df_scored[f'score_{criterion}'] = contribution
            breakdown_parts.append(criterion)
        
        # Apply sustainability bonus if enabled
        bonus_config = self.advanced_config.get('sustainability_bonus', {})
        if bonus_config.get('enabled', False):
            bonus_threshold = bonus_config.get('recyclability_threshold', 80.0)
            bonus_multiplier = bonus_config.get('bonus_multiplier', 1.1)
            
            bonus_mask = df_scored['recyclability_percent'] >= bonus_threshold
            bonus_count = bonus_mask.sum()
            
            if bonus_count > 0:
                df_scored.loc[bonus_mask, 'ranking_score'] *= bonus_multiplier
                df_scored.loc[bonus_mask, 'sustainability_bonus_applied'] = True
                logger.info(f"Applied sustainability bonus to {bonus_count} materials with recyclability >= {bonus_threshold}%")
            
            df_scored['sustainability_bonus_applied'] = df_scored.get('sustainability_bonus_applied', False)
        
        # Ensure score is in [0, 1] range
        df_scored['ranking_score'] = df_scored['ranking_score'].clip(0, 1)
        
        return df_scored
    
    def rank_materials(self, df: pd.DataFrame, group_by: Optional[str] = None) -> pd.DataFrame:
        """
        Rank materials based on composite scores
        
        Args:
            df: DataFrame with materials and features
            group_by: Optional column to group by (e.g., 'product_id', 'packaging_type')
            
        Returns:
            DataFrame with ranked materials
        """
        # Apply constraints first
        df_valid = self.apply_constraints(df)
        
        if len(df_valid) == 0:
            logger.warning("No materials passed constraint filtering!")
            return pd.DataFrame()
        
        # Calculate ranking scores
        df_ranked = self.calculate_ranking_score(df_valid)
        
        # Rank materials
        if group_by and group_by in df_ranked.columns:
            # Rank within groups
            df_ranked['rank'] = df_ranked.groupby(group_by)['ranking_score'].rank(
                ascending=False, method='dense'
            ).astype(int)
            
            # Sort by group and rank
            df_ranked = df_ranked.sort_values([group_by, 'rank'])
            
            logger.info(f"Ranked materials within {df_ranked[group_by].nunique()} groups")
        else:
            # Global ranking
            df_ranked['rank'] = df_ranked['ranking_score'].rank(
                ascending=False, method='dense'
            ).astype(int)
            
            # Sort by rank
            df_ranked = df_ranked.sort_values('rank')
            
            logger.info(f"Ranked {len(df_ranked)} materials globally")
        
        return df_ranked
    
    def get_top_recommendations(
        self, 
        df_ranked: pd.DataFrame, 
        top_n: Optional[int] = None,
        group_by: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get top N recommended materials
        
        Args:
            df_ranked: DataFrame with ranked materials
            top_n: Number of top materials to return (default from config)
            group_by: Optional column to group by
            
        Returns:
            DataFrame with top N materials
        """
        if top_n is None:
            top_n = self.output_config.get('top_n_recommendations', 5)
        
        if group_by and group_by in df_ranked.columns:
            # Get top N per group
            top_materials = df_ranked.groupby(group_by).head(top_n)
            logger.info(f"Retrieved top {top_n} materials per group")
        else:
            # Get top N globally
            top_materials = df_ranked.head(top_n)
            logger.info(f"Retrieved top {top_n} materials")
        
        return top_materials
    
    def generate_explanation(self, material_row: pd.Series) -> str:
        """
        Generate human-readable explanation for a material's ranking
        
        Args:
            material_row: Series with material data
            
        Returns:
            Explanation string
        """
        explanation_parts = []
        
        # Overall rank and score
        rank = material_row.get('rank', 'N/A')
        score = material_row.get('ranking_score', 0)
        explanation_parts.append(f"Rank #{rank} with score {score:.3f}")
        
        # Breakdown by criteria
        criteria_explanations = []
        for criterion, weight in self.weights.items():
            score_col = f'score_{criterion}'
            if score_col in material_row:
                contribution = material_row[score_col]
                criteria_explanations.append(f"{criterion}: {contribution:.3f} ({weight*100:.0f}%)")
        
        if criteria_explanations:
            explanation_parts.append("Breakdown: " + ", ".join(criteria_explanations))
        
        # Key metrics
        metrics = []
        if 'predicted_cost' in material_row:
            metrics.append(f"Cost: ${material_row['predicted_cost']:.2f}")
        if 'predicted_co2' in material_row:
            metrics.append(f"CO₂: {material_row['predicted_co2']:.2f} kg")
        if 'material_suitability_score' in material_row:
            metrics.append(f"Suitability: {material_row['material_suitability_score']:.1f}")
        if 'recyclability_percent' in material_row:
            metrics.append(f"Recyclability: {material_row['recyclability_percent']:.1f}%")
        
        if metrics:
            explanation_parts.append("Metrics: " + ", ".join(metrics))
        
        # Bonus
        if material_row.get('sustainability_bonus_applied', False):
            explanation_parts.append("✓ Sustainability bonus applied")
        
        return " | ".join(explanation_parts)
    
    def export_rankings(
        self, 
        df_ranked: pd.DataFrame, 
        output_path: str,
        format: str = 'csv',
        include_explanations: bool = None
    ):
        """
        Export ranked materials to file
        
        Args:
            df_ranked: DataFrame with ranked materials
            output_path: Path to save output file
            format: Export format ('csv', 'json', 'excel')
            include_explanations: Whether to include explanations
        """
        if include_explanations is None:
            include_explanations = self.output_config.get('include_explanations', True)
        
        # Select output columns
        output_columns = self.output_config.get('output_columns', [])
        available_columns = [col for col in output_columns if col in df_ranked.columns]
        
        # Add all columns if none specified
        if not available_columns:
            available_columns = df_ranked.columns.tolist()
        
        df_export = df_ranked[available_columns].copy()
        
        # Add explanations if requested
        if include_explanations:
            df_export['explanation'] = df_ranked.apply(self.generate_explanation, axis=1)
        
        # Export based on format
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'csv':
            df_export.to_csv(output_path, index=False)
            logger.info(f"Rankings exported to {output_path}")
            
        elif format == 'json':
            df_export.to_json(output_path, orient='records', indent=2)
            logger.info(f"Rankings exported to {output_path}")
            
        elif format == 'excel':
            df_export.to_excel(output_path, index=False, engine='openpyxl')
            logger.info(f"Rankings exported to {output_path}")
            
        else:
            logger.error(f"Unsupported export format: {format}")
            raise ValueError(f"Unsupported format: {format}")
    
    def run_ranking_pipeline(
        self,
        data_path: str,
        predictions_path: Optional[str] = None,
        output_path: str = 'outputs/material_rankings.csv',
        group_by: Optional[str] = None,
        top_n: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Run complete ranking pipeline
        
        Args:
            data_path: Path to feature dataset
            predictions_path: Optional path to predictions CSV
            output_path: Path to save rankings
            group_by: Optional column to group by
            top_n: Number of top materials per group
            
        Returns:
            DataFrame with ranked materials
        """
        logger.info("Starting material ranking pipeline...")
        
        # Load data
        logger.info(f"Loading data from {data_path}")
        df = pd.read_csv(data_path)
        logger.info(f"Loaded {len(df)} materials")
        
        # Load predictions if provided
        if predictions_path and Path(predictions_path).exists():
            logger.info(f"Loading predictions from {predictions_path}")
            predictions = pd.read_csv(predictions_path)
            
            # Merge predictions with features
            if 'predicted_cost' in predictions.columns:
                df['predicted_cost'] = predictions['predicted_cost']
            if 'predicted_co2' in predictions.columns:
                df['predicted_co2'] = predictions['predicted_co2']
        
        # Rank materials
        df_ranked = self.rank_materials(df, group_by=group_by)
        
        if len(df_ranked) == 0:
            logger.error("No materials to rank after filtering!")
            return pd.DataFrame()
        
        # Get top recommendations
        df_top = self.get_top_recommendations(df_ranked, top_n=top_n, group_by=group_by)
        
        # Export results
        self.export_rankings(df_top, output_path)
        
        # Log summary statistics
        logger.info("=" * 60)
        logger.info("RANKING SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Ranking mode: {self.ranking_mode}")
        logger.info(f"Total materials evaluated: {len(df)}")
        logger.info(f"Materials after filtering: {len(df_ranked)}")
        logger.info(f"Top recommendations: {len(df_top)}")
        logger.info(f"Average ranking score: {df_ranked['ranking_score'].mean():.3f}")
        logger.info(f"Score range: [{df_ranked['ranking_score'].min():.3f}, {df_ranked['ranking_score'].max():.3f}]")
        logger.info("=" * 60)
        
        return df_top


def main():
    """Example usage of MaterialRanker"""
    # Initialize ranker
    ranker = MaterialRanker(
        config_path='config/ranking_weights.yaml',
        ranking_mode='balanced'
    )
    
    # Run ranking pipeline
    df_ranked = ranker.run_ranking_pipeline(
        data_path='data/ml_ready/X_raw.csv',
        predictions_path=None,  # Will be added when we have predictions
        output_path='outputs/material_rankings.csv',
        group_by=None,  # Can group by 'packaging_type' or other columns
        top_n=10
    )
    
    print("\nTop 5 Recommended Materials:")
    print(df_ranked.head())


if __name__ == '__main__':
    main()
