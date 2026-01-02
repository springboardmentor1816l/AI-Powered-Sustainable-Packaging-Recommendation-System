"""
SHAP Explainability Module
===========================

This module uses SHAP (SHapley Additive exPlanations) to explain model predictions
and identify feature importance at both global and local levels.

Author: EcoPackAI Team
Date: 2026-01-02
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import pickle
import shap
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import logging
import warnings

warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style for visualizations
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


class SHAPExplainer:
    """
    SHAP-based Model Explainer
    
    Provides comprehensive model interpretation using SHAP values including:
    - Global feature importance
    - Local prediction explanations
    - Feature interactions
    - Summary plots and visualizations
    """
    
    def __init__(
        self,
        model,
        model_type: str = 'tree',
        feature_names: Optional[List[str]] = None
    ):
        """
        Initialize SHAP Explainer
        
        Args:
            model: Trained ML model
            model_type: Type of model ('tree', 'linear', 'kernel')
            feature_names: List of feature names
        """
        self.model = model
        self.model_type = model_type
        self.feature_names = feature_names
        self.explainer = None
        self.shap_values = None
        self.base_value = None
        
        logger.info(f"Initialized SHAP Explainer for {model_type} model")
    
    def create_explainer(self, X_background: pd.DataFrame):
        """
        Create SHAP explainer appropriate for model type
        
        Args:
            X_background: Background dataset for SHAP estimation
        """
        logger.info("Creating SHAP explainer...")
        
        try:
            if self.model_type == 'tree':
                # For tree-based models (Random Forest, XGBoost)
                self.explainer = shap.TreeExplainer(
                    self.model,
                    feature_perturbation='interventional'
                )
                logger.info("Created TreeExplainer")
                
            elif self.model_type == 'linear':
                # For linear models
                self.explainer = shap.LinearExplainer(
                    self.model,
                    X_background
                )
                logger.info("Created LinearExplainer")
                
            else:
                # For model-agnostic explanation
                self.explainer = shap.KernelExplainer(
                    self.model.predict,
                    shap.sample(X_background, 100)
                )
                logger.info("Created KernelExplainer")
                
        except Exception as e:
            logger.error(f"Error creating explainer: {e}")
            raise
    
    def calculate_shap_values(
        self,
        X: pd.DataFrame,
        max_samples: Optional[int] = None
    ) -> np.ndarray:
        """
        Calculate SHAP values for dataset
        
        Args:
            X: Input features
            max_samples: Maximum samples to explain (for performance)
            
        Returns:
            SHAP values array
        """
        if self.explainer is None:
            raise ValueError("Explainer not created. Call create_explainer() first.")
        
        logger.info(f"Calculating SHAP values for {len(X)} samples...")
        
        # Limit samples if specified
        if max_samples and len(X) > max_samples:
            X_sample = X.sample(n=max_samples, random_state=42)
            logger.info(f"Sampled {max_samples} instances for SHAP calculation")
        else:
            X_sample = X
        
        try:
            if self.model_type == 'tree':
                # TreeExplainer returns different formats for different models
                shap_output = self.explainer.shap_values(X_sample)
                
                # Handle multi-output case (classification)
                if isinstance(shap_output, list):
                    # For multi-class, take first class or average
                    self.shap_values = shap_output[0]
                else:
                    self.shap_values = shap_output
                    
                self.base_value = self.explainer.expected_value
                if isinstance(self.base_value, (list, np.ndarray)):
                    self.base_value = self.base_value[0]
                    
            else:
                shap_output = self.explainer.shap_values(X_sample)
                self.shap_values = shap_output
                self.base_value = self.explainer.expected_value
            
            logger.info(f"✓ Calculated SHAP values shape: {self.shap_values.shape}")
            return self.shap_values
            
        except Exception as e:
            logger.error(f"Error calculating SHAP values: {e}")
            raise
    
    def get_feature_importance(
        self,
        method: str = 'mean_abs'
    ) -> pd.DataFrame:
        """
        Get global feature importance from SHAP values
        
        Args:
            method: Aggregation method ('mean_abs', 'mean', 'max')
            
        Returns:
            DataFrame with feature importance scores
        """
        if self.shap_values is None:
            raise ValueError("SHAP values not calculated. Call calculate_shap_values() first.")
        
        if method == 'mean_abs':
            importance = np.abs(self.shap_values).mean(axis=0)
        elif method == 'mean':
            importance = self.shap_values.mean(axis=0)
        elif method == 'max':
            importance = np.abs(self.shap_values).max(axis=0)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        # Create DataFrame
        if self.feature_names:
            feature_names = self.feature_names
        else:
            feature_names = [f"Feature_{i}" for i in range(len(importance))]
        
        df_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        return df_importance
    
    def plot_summary(
        self,
        X: pd.DataFrame,
        plot_type: str = 'dot',
        max_display: int = 20,
        output_path: Optional[str] = None
    ):
        """
        Create SHAP summary plot
        
        Args:
            X: Input features
            plot_type: Type of plot ('dot', 'bar', 'violin')
            max_display: Maximum features to display
            output_path: Path to save plot
        """
        if self.shap_values is None:
            raise ValueError("SHAP values not calculated.")
        
        logger.info(f"Creating SHAP summary plot ({plot_type})...")
        
        plt.figure(figsize=(12, 8))
        
        try:
            shap.summary_plot(
                self.shap_values,
                X,
                plot_type=plot_type,
                max_display=max_display,
                show=False
            )
            
            plt.title(f"SHAP Summary Plot - Feature Impact on Predictions", 
                     fontsize=14, fontweight='bold', pad=20)
            plt.xlabel("SHAP Value (impact on model output)", fontsize=12)
            plt.tight_layout()
            
            if output_path:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                logger.info(f"✓ Saved summary plot to {output_path}")
            
            plt.close()
            
        except Exception as e:
            logger.error(f"Error creating summary plot: {e}")
            plt.close()
            raise
    
    def plot_bar(
        self,
        max_display: int = 15,
        output_path: Optional[str] = None
    ):
        """
        Create bar plot of feature importance
        
        Args:
            max_display: Maximum features to display
            output_path: Path to save plot
        """
        if self.shap_values is None:
            raise ValueError("SHAP values not calculated.")
        
        logger.info("Creating SHAP bar plot...")
        
        plt.figure(figsize=(10, 8))
        
        try:
            shap.summary_plot(
                self.shap_values,
                features=None,
                feature_names=self.feature_names,
                plot_type='bar',
                max_display=max_display,
                show=False
            )
            
            plt.title(f"Global Feature Importance - Mean |SHAP|", 
                     fontsize=14, fontweight='bold', pad=20)
            plt.xlabel("Mean |SHAP value|", fontsize=12)
            plt.tight_layout()
            
            if output_path:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                logger.info(f"✓ Saved bar plot to {output_path}")
            
            plt.close()
            
        except Exception as e:
            logger.error(f"Error creating bar plot: {e}")
            plt.close()
            raise
    
    def plot_waterfall(
        self,
        instance_index: int,
        X: pd.DataFrame,
        output_path: Optional[str] = None
    ):
        """
        Create waterfall plot for single prediction explanation
        
        Args:
            instance_index: Index of instance to explain
            X: Input features
            output_path: Path to save plot
        """
        if self.shap_values is None:
            raise ValueError("SHAP values not calculated.")
        
        logger.info(f"Creating waterfall plot for instance {instance_index}...")
        
        plt.figure(figsize=(10, 8))
        
        try:
            # Create explanation object
            explanation = shap.Explanation(
                values=self.shap_values[instance_index],
                base_values=self.base_value,
                data=X.iloc[instance_index].values,
                feature_names=self.feature_names if self.feature_names else X.columns.tolist()
            )
            
            shap.waterfall_plot(explanation, show=False)
            
            plt.title(f"SHAP Waterfall Plot - Instance {instance_index}", 
                     fontsize=14, fontweight='bold', pad=20)
            plt.tight_layout()
            
            if output_path:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                logger.info(f"✓ Saved waterfall plot to {output_path}")
            
            plt.close()
            
        except Exception as e:
            logger.error(f"Error creating waterfall plot: {e}")
            plt.close()
            raise
    
    def plot_force(
        self,
        instance_index: int,
        X: pd.DataFrame,
        output_path: Optional[str] = None,
        matplotlib: bool = True
    ):
        """
        Create force plot for single prediction
        
        Args:
            instance_index: Index of instance to explain
            X: Input features
            output_path: Path to save plot
            matplotlib: Use matplotlib backend (True) or JavaScript (False)
        """
        if self.shap_values is None:
            raise ValueError("SHAP values not calculated.")
        
        logger.info(f"Creating force plot for instance {instance_index}...")
        
        try:
            if matplotlib:
                plt.figure(figsize=(20, 3))
                shap.force_plot(
                    self.base_value,
                    self.shap_values[instance_index],
                    X.iloc[instance_index],
                    matplotlib=True,
                    show=False
                )
                
                plt.title(f"SHAP Force Plot - Instance {instance_index}", 
                         fontsize=12, fontweight='bold')
                plt.tight_layout()
                
                if output_path:
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    plt.savefig(output_path, dpi=300, bbox_inches='tight')
                    logger.info(f"✓ Saved force plot to {output_path}")
                
                plt.close()
            else:
                # JavaScript version
                force_plot = shap.force_plot(
                    self.base_value,
                    self.shap_values[instance_index],
                    X.iloc[instance_index]
                )
                
                if output_path:
                    shap.save_html(output_path, force_plot)
                    logger.info(f"✓ Saved interactive force plot to {output_path}")
                    
        except Exception as e:
            logger.error(f"Error creating force plot: {e}")
            if matplotlib:
                plt.close()
            raise
    
    def plot_dependence(
        self,
        feature: str,
        X: pd.DataFrame,
        interaction_feature: Optional[str] = 'auto',
        output_path: Optional[str] = None
    ):
        """
        Create dependence plot showing feature effect
        
        Args:
            feature: Feature to analyze
            X: Input features
            interaction_feature: Feature for interaction coloring
            output_path: Path to save plot
        """
        if self.shap_values is None:
            raise ValueError("SHAP values not calculated.")
        
        logger.info(f"Creating dependence plot for '{feature}'...")
        
        plt.figure(figsize=(10, 6))
        
        try:
            shap.dependence_plot(
                feature,
                self.shap_values,
                X,
                interaction_index=interaction_feature,
                show=False
            )
            
            plt.title(f"SHAP Dependence Plot - {feature}", 
                     fontsize=14, fontweight='bold', pad=20)
            plt.tight_layout()
            
            if output_path:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                logger.info(f"✓ Saved dependence plot to {output_path}")
            
            plt.close()
            
        except Exception as e:
            logger.error(f"Error creating dependence plot: {e}")
            plt.close()
            raise
    
    def analyze_feature_interactions(
        self,
        X: pd.DataFrame,
        top_n: int = 5
    ) -> pd.DataFrame:
        """
        Analyze feature interactions
        
        Args:
            X: Input features
            top_n: Number of top features to analyze
            
        Returns:
            DataFrame with interaction scores
        """
        if self.shap_values is None:
            raise ValueError("SHAP values not calculated.")
        
        logger.info("Analyzing feature interactions...")
        
        # Get top features
        top_features = self.get_feature_importance().head(top_n)['feature'].tolist()
        
        interactions = []
        
        for i, feat1 in enumerate(top_features):
            for feat2 in top_features[i+1:]:
                # Calculate interaction strength
                idx1 = self.feature_names.index(feat1)
                idx2 = self.feature_names.index(feat2)
                
                interaction_strength = np.abs(
                    self.shap_values[:, idx1] * self.shap_values[:, idx2]
                ).mean()
                
                interactions.append({
                    'feature_1': feat1,
                    'feature_2': feat2,
                    'interaction_strength': interaction_strength
                })
        
        df_interactions = pd.DataFrame(interactions).sort_values(
            'interaction_strength', ascending=False
        )
        
        return df_interactions
    
    def generate_report(
        self,
        X: pd.DataFrame,
        output_dir: str,
        model_name: str = "model"
    ) -> Dict:
        """
        Generate comprehensive SHAP analysis report
        
        Args:
            X: Input features
            output_dir: Directory to save outputs
            model_name: Name of model for file naming
            
        Returns:
            Dictionary with analysis results
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Generating SHAP Report for {model_name}")
        logger.info(f"{'='*60}\n")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = {}
        
        # 1. Feature importance
        logger.info("1. Calculating feature importance...")
        feature_importance = self.get_feature_importance()
        results['feature_importance'] = feature_importance
        
        # Save to CSV
        feature_importance.to_csv(
            output_path / f"{model_name}_feature_importance.csv",
            index=False
        )
        logger.info(f"   ✓ Saved feature importance")
        
        # 2. Summary plot
        logger.info("2. Creating summary plot...")
        self.plot_summary(
            X,
            plot_type='dot',
            max_display=20,
            output_path=output_path / f"{model_name}_shap_summary.png"
        )
        
        # 3. Bar plot
        logger.info("3. Creating bar plot...")
        self.plot_bar(
            max_display=15,
            output_path=output_path / f"{model_name}_feature_importance.png"
        )
        
        # 4. Waterfall for top prediction
        logger.info("4. Creating waterfall plot...")
        self.plot_waterfall(
            instance_index=0,
            X=X,
            output_path=output_path / f"{model_name}_waterfall_example.png"
        )
        
        # 5. Dependence plots for top 3 features
        logger.info("5. Creating dependence plots...")
        top_3_features = feature_importance.head(3)['feature'].tolist()
        for feature in top_3_features:
            try:
                self.plot_dependence(
                    feature,
                    X,
                    output_path=output_path / f"{model_name}_dependence_{feature}.png"
                )
            except Exception as e:
                logger.warning(f"   Could not create dependence plot for {feature}: {e}")
        
        # 6. Feature interactions
        logger.info("6. Analyzing feature interactions...")
        try:
            interactions = self.analyze_feature_interactions(X, top_n=5)
            results['interactions'] = interactions
            interactions.to_csv(
                output_path / f"{model_name}_interactions.csv",
                index=False
            )
            logger.info(f"   ✓ Saved interaction analysis")
        except Exception as e:
            logger.warning(f"   Could not analyze interactions: {e}")
        
        logger.info(f"\n{'='*60}")
        logger.info(f"✓ SHAP Report Generated Successfully")
        logger.info(f"Output directory: {output_path}")
        logger.info(f"{'='*60}\n")
        
        return results


def load_model_and_explain(
    model_path: str,
    data_path: str,
    model_type: str,
    target_col: str,
    output_dir: str,
    model_name: str,
    max_samples: int = 500
):
    """
    Convenience function to load model and generate SHAP explanations
    
    Args:
        model_path: Path to saved model
        data_path: Path to data CSV
        model_type: Type of model ('tree', 'linear')
        target_col: Target column name
        output_dir: Output directory
        model_name: Model name for files
        max_samples: Maximum samples for SHAP calculation
    """
    logger.info(f"Loading model from {model_path}...")
    
    # Load model
    if model_path.endswith('.pkl'):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
    else:
        model = joblib.load(model_path)
    
    logger.info(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    
    # Separate features and target
    if target_col in df.columns:
        X = df.drop(columns=[target_col])
    else:
        X = df
    
    logger.info(f"Data shape: {X.shape}")
    
    # Initialize explainer
    explainer = SHAPExplainer(
        model=model,
        model_type=model_type,
        feature_names=X.columns.tolist()
    )
    
    # Create explainer
    explainer.create_explainer(X.head(100))
    
    # Calculate SHAP values
    explainer.calculate_shap_values(X, max_samples=max_samples)
    
    # Generate report
    results = explainer.generate_report(X, output_dir, model_name)
    
    return explainer, results
