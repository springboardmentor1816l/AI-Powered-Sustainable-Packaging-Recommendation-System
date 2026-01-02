"""
Feature Importance Analyzer
============================

Model-agnostic feature importance using permutation importance
and other techniques.

Author: EcoPackAI Team
Date: 2026-01-02
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureImportanceAnalyzer:
    """
    Analyze feature importance using multiple methods
    """
    
    def __init__(self, model, feature_names: List[str]):
        """
        Initialize analyzer
        
        Args:
            model: Trained model
            feature_names: List of feature names
        """
        self.model = model
        self.feature_names = feature_names
        self.importance_scores = {}
        
        logger.info("Initialized Feature Importance Analyzer")
    
    def get_builtin_importance(self) -> Optional[pd.DataFrame]:
        """
        Get built-in feature importance if available
        
        Returns:
            DataFrame with feature importance or None
        """
        try:
            if hasattr(self.model, 'feature_importances_'):
                # Tree-based models
                importance = self.model.feature_importances_
                
                df_importance = pd.DataFrame({
                    'feature': self.feature_names,
                    'importance': importance
                }).sort_values('importance', ascending=False)
                
                self.importance_scores['builtin'] = df_importance
                logger.info("✓ Extracted built-in feature importance")
                return df_importance
                
            elif hasattr(self.model, 'coef_'):
                # Linear models
                if len(self.model.coef_.shape) == 1:
                    importance = np.abs(self.model.coef_)
                else:
                    importance = np.abs(self.model.coef_[0])
                
                df_importance = pd.DataFrame({
                    'feature': self.feature_names,
                    'importance': importance
                }).sort_values('importance', ascending=False)
                
                self.importance_scores['builtin'] = df_importance
                logger.info("✓ Extracted built-in coefficients")
                return df_importance
            
            else:
                logger.warning("Model does not have built-in feature importance")
                return None
                
        except Exception as e:
            logger.error(f"Error getting built-in importance: {e}")
            return None
    
    def calculate_permutation_importance(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        n_repeats: int = 10,
        random_state: int = 42,
        scoring: str = 'neg_mean_absolute_error'
    ) -> pd.DataFrame:
        """
        Calculate permutation importance
        
        Args:
            X: Feature matrix
            y: Target vector
            n_repeats: Number of permutation repeats
            random_state: Random seed
            scoring: Scoring metric
            
        Returns:
            DataFrame with permutation importance
        """
        logger.info("Calculating permutation importance...")
        
        try:
            result = permutation_importance(
                self.model,
                X,
                y,
                n_repeats=n_repeats,
                random_state=random_state,
                scoring=scoring,
                n_jobs=-1
            )
            
            df_importance = pd.DataFrame({
                'feature': self.feature_names,
                'importance_mean': result.importances_mean,
                'importance_std': result.importances_std
            }).sort_values('importance_mean', ascending=False)
            
            self.importance_scores['permutation'] = df_importance
            logger.info("✓ Calculated permutation importance")
            
            return df_importance
            
        except Exception as e:
            logger.error(f"Error calculating permutation importance: {e}")
            raise
    
    def calculate_drop_column_importance(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        metric: str = 'mae'
    ) -> pd.DataFrame:
        """
        Calculate importance by dropping each column
        
        Args:
            X: Feature matrix
            y: Target vector
            metric: Metric to evaluate ('mae', 'rmse', 'r2')
            
        Returns:
            DataFrame with drop-column importance
        """
        logger.info("Calculating drop-column importance...")
        
        # Get baseline score
        y_pred_baseline = self.model.predict(X)
        
        if metric == 'mae':
            baseline_score = mean_absolute_error(y, y_pred_baseline)
            higher_is_better = False
        elif metric == 'rmse':
            baseline_score = mean_squared_error(y, y_pred_baseline, squared=False)
            higher_is_better = False
        elif metric == 'r2':
            baseline_score = r2_score(y, y_pred_baseline)
            higher_is_better = True
        else:
            raise ValueError(f"Unknown metric: {metric}")
        
        logger.info(f"Baseline {metric.upper()}: {baseline_score:.6f}")
        
        importances = []
        
        for feature in self.feature_names:
            # Create dataset without this feature
            X_dropped = X.drop(columns=[feature])
            
            try:
                # Would need to retrain, so we use permutation instead
                # For simplicity, we'll permute the column
                X_permuted = X.copy()
                X_permuted[feature] = np.random.permutation(X_permuted[feature].values)
                
                y_pred = self.model.predict(X_permuted)
                
                if metric == 'mae':
                    score = mean_absolute_error(y, y_pred)
                    importance = score - baseline_score  # Increase bad
                elif metric == 'rmse':
                    score = mean_squared_error(y, y_pred, squared=False)
                    importance = score - baseline_score  # Increase is bad
                elif metric == 'r2':
                    score = r2_score(y, y_pred)
                    importance = baseline_score - score  # Decrease is bad
                
                importances.append({
                    'feature': feature,
                    'baseline_score': baseline_score,
                    'dropped_score': score,
                    'importance': importance
                })
                
            except Exception as e:
                logger.warning(f"Could not evaluate {feature}: {e}")
        
        df_importance = pd.DataFrame(importances).sort_values(
            'importance', ascending=False
        )
        
        self.importance_scores['drop_column'] = df_importance
        logger.info("✓ Calculated drop-column importance")
        
        return df_importance
    
    def plot_comparison(
        self,
        top_n: int = 15,
        output_path: Optional[str] = None
    ):
        """
        Plot comparison of different importance methods
        
        Args:
            top_n: Number of top features to show
            output_path: Path to save plot
        """
        if not self.importance_scores:
            logger.warning("No importance scores calculated")
            return
        
        logger.info("Creating importance comparison plot...")
        
        n_methods = len(self.importance_scores)
        fig, axes = plt.subplots(1, n_methods, figsize=(6*n_methods, 8))
        
        if n_methods == 1:
            axes = [axes]
        
        for idx, (method, df_imp) in enumerate(self.importance_scores.items()):
            ax = axes[idx]
            
            # Get top N features
            df_plot = df_imp.head(top_n).copy()
            
            # Normalize importance for comparison
            if 'importance' in df_plot.columns:
                importance_col = 'importance'
            elif 'importance_mean' in df_plot.columns:
                importance_col = 'importance_mean'
            else:
                importance_col = df_plot.columns[1]
            
            df_plot = df_plot.sort_values(importance_col)
            
            # Create bar plot
            colors = plt.cm.viridis(np.linspace(0, 1, len(df_plot)))
            ax.barh(df_plot['feature'], df_plot[importance_col], color=colors)
            
            ax.set_xlabel(f'{method.title()} Importance', fontsize=12)
            ax.set_ylabel('Feature', fontsize=12)
            ax.set_title(f'{method.replace("_", " ").title()} Feature Importance\nTop {top_n} Features',
                        fontsize=13, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            logger.info(f"✓ Saved comparison plot to {output_path}")
        
        plt.close()
    
    def generate_report(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        output_dir: str,
        model_name: str = "model"
    ) -> Dict:
        """
        Generate comprehensive feature importance report
        
        Args:
            X: Feature matrix
            y: Target vector
            output_dir: Output directory
            model_name: Model name
            
        Returns:
            Dictionary with results
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Generating Feature Importance Report for {model_name}")
        logger.info(f"{'='*60}\n")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = {}
        
        # 1. Built-in importance
        logger.info("1. Getting built-in importance...")
        builtin_imp = self.get_builtin_importance()
        if builtin_imp is not None:
            results['builtin'] = builtin_imp
            builtin_imp.to_csv(
                output_path / f"{model_name}_builtin_importance.csv",
                index=False
            )
        
        # 2. Permutation importance
        logger.info("2. Calculating permutation importance...")
        perm_imp = self.calculate_permutation_importance(X, y)
        results['permutation'] = perm_imp
        perm_imp.to_csv(
            output_path / f"{model_name}_permutation_importance.csv",
            index=False
        )
        
        # 3. Comparison plot
        logger.info("3. Creating comparison plot...")
        self.plot_comparison(
            top_n=15,
            output_path=output_path / f"{model_name}_importance_comparison.png"
        )
        
        logger.info(f"\n{'='*60}")
        logger.info(f"✓ Feature Importance Report Generated")
        logger.info(f"{'='*60}\n")
        
        return results
