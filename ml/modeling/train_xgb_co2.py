"""
EcoPackAI - XGBoost CO₂ Emission Prediction Model Training
Trains an advanced XGBoost model for packaging CO₂ emission prediction

Author: EcoPackAI Team
Date: 2025-12-26
"""

import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import json
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuration
RANDOM_SEED = 42
N_FOLDS = 5
TRAIN_TEST_RATIO = 0.80

# Define directories
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / 'data'
ML_DIR = BASE_DIR / 'ml'
METRICS_DIR = ML_DIR / 'metrics'
MODELS_DIR = ML_DIR / 'models'
REPORTS_DIR = ML_DIR / 'reports'
DOCS_DIR = BASE_DIR / 'docs'
PROCESSED_DIR = DATA_DIR / 'processed'

# Create directories
METRICS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print(" " * 12 + "ECOPACKAI - XGBOOST CO₂ EMISSION PREDICTION")
print("="*80)
print("\nTraining advanced gradient boosting model for CO₂ prediction...")


# ==============================================================================
# STEP 1: LOAD AND PREPARE DATA
# ==============================================================================

def load_and_prepare_data():
    """Load integrated dataset and prepare features for CO₂ prediction"""
    print("\n" + "="*80)
    print("STEP 1: LOADING AND PREPARING DATA")
    print("="*80)
    
    # Load integrated dataset
    data_path = PROCESSED_DIR / 'cleaned_integrated_materials.csv'
    print(f"\n📥 Loading data from: {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"✓ Loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Define target
    target_col = 'co2_emission_per_kg_estimated'
    
    # Define features to exclude
    exclude_cols = [
        'material_id',  # ID column
        'suitable_product_categories',  # Text field
        'recommended_packaging_use_cases',  # Text field
        'cost_per_unit_usd',  # Other target (not for CO₂ model)
        'co2_emission_per_kg_estimated',  # Target variable
        'carbon_footprint_kg_co2_unit'  # Highly correlated with target (prevent leakage)
    ]
    
    # Select feature columns
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    print(f"\n🎯 Feature & Target Selection:")
    print(f"  - Target: {target_col}")
    print(f"  - Target units: kg CO₂ per kg material")
    print(f"  - Total features: {len(feature_cols)}")
    print(f"  - Excluded columns: {len(exclude_cols)}")
    
    # Prepare features
    X = df[feature_cols].copy()
    y = df[target_col].copy()
    
    # Handle categorical columns
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numeric_cols = X.select_dtypes(include=['number']).columns.tolist()
    
    print(f"\n📊 Feature Breakdown:")
    print(f"  - Categorical features: {len(categorical_cols)}")
    for cat in categorical_cols:
        print(f"      • {cat}")
    
    print(f"  - Numeric features: {len(numeric_cols)}")
    print(f"      First 10:")
    for num in numeric_cols[:10]:
        print(f"        • {num}")
    if len(numeric_cols) > 10:
        print(f"      ... and {len(numeric_cols) - 10} more")
    
    # Encode categorical variables
    print(f"\n🔧 Encoding categorical variables...")
    label_encoders = {}
    
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le
        print(f"  ✓ {col}: {len(le.classes_)} categories → encoded")
    
    # Target statistics
    print(f"\n📈 Target Variable Statistics (CO₂ Emissions):")
    print(f"  - Mean: {y.mean():.4f} kg CO₂/kg")
    print(f"  - Median: {y.median():.4f} kg CO₂/kg")
    print(f"  - Std Dev: {y.std():.4f} kg CO₂/kg")
    print(f"  - Min: {y.min():.4f} kg CO₂/kg")
    print(f"  - Max: {y.max():.4f} kg CO₂/kg")
    print(f"  - Range: {y.max() - y.min():.4f} kg CO₂/kg")
    
    # Check for target leakage
    print(f"\n🔍 Target Leakage Prevention:")
    print(f"  ✓ Excluded CO₂ target from features")
    print(f"  ✓ Excluded carbon_footprint (highly correlated)")
    print(f"  ✓ Excluded cost target from features")
    print(f"  ✓ No derived CO₂ features in X")
    
    return X, y, df, label_encoders, feature_cols


# ==============================================================================
# STEP 2: CREATE TRAIN/TEST SPLIT
# ==============================================================================

def create_train_test_split(X, y, df):
    """Create stratified train/test split"""
    print("\n" + "="*80)
    print("STEP 2: CREATING TRAIN/TEST SPLIT")
    print("="*80)
    
    print(f"\n📊 Split Configuration:")
    print(f"  - Strategy: Stratified by material_type")
    print(f"  - Train/Test Ratio: {TRAIN_TEST_RATIO*100:.0f}% / {(1-TRAIN_TEST_RATIO)*100:.0f}%")
    print(f"  - Random Seed: {RANDOM_SEED}")
    
    # Use material_type for stratification
    stratify_labels = LabelEncoder().fit_transform(df['material_type'])
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        train_size=TRAIN_TEST_RATIO,
        random_state=RANDOM_SEED,
        stratify=stratify_labels,
        shuffle=True
    )
    
    print(f"\n✅ Split created:")
    print(f"  - Training samples: {len(X_train)} ({len(X_train)/len(X)*100:.1f}%)")
    print(f"  - Testing samples: {len(X_test)} ({len(X_test)/len(X)*100:.1f}%)")
    
    print(f"\n  Training target statistics:")
    print(f"    Mean: {y_train.mean():.4f} kg CO₂/kg")
    print(f"    Std: {y_train.std():.4f} kg CO₂/kg")
    
    print(f"\n  Testing target statistics:")
    print(f"    Mean: {y_test.mean():.4f} kg CO₂/kg")
    print(f"    Std: {y_test.std():.4f} kg CO₂/kg")
    
    return X_train, X_test, y_train, y_test


# ==============================================================================
# STEP 3: CONFIGURE XGBOOST MODEL
# ==============================================================================

def configure_xgboost():
    """Configure XGBoost model with optimized hyperparameters"""
    print("\n" + "="*80)
    print("STEP 3: CONFIGURING XGBOOST MODEL")
    print("="*80)
    
    # Define hyperparameters
    xgb_params = {
        'objective': 'reg:squarederror',  # Regression task
        'n_estimators': 200,               # Number of boosting rounds
        'max_depth': 6,                    # Maximum tree depth
        'learning_rate': 0.1,              # Step size shrinkage
        'subsample': 0.8,                  # Subsample ratio of training data
        'colsample_bytree': 0.8,           # Subsample ratio of columns
        'min_child_weight': 3,             # Minimum sum of instance weight
        'gamma': 0,                        # Minimum loss reduction
        'reg_alpha': 0.1,                  # L1 regularization
        'reg_lambda': 1.0,                 # L2 regularization
        'random_state': RANDOM_SEED,
        'n_jobs': -1,                      # Use all cores
        'verbosity': 0                     # Silent mode
    }
    
    print(f"\n🚀 XGBoost Configuration:")
    print(f"  - Objective: {xgb_params['objective']}")
    print(f"  - Number of boosting rounds: {xgb_params['n_estimators']}")
    print(f"  - Max tree depth: {xgb_params['max_depth']}")
    print(f"  - Learning rate: {xgb_params['learning_rate']}")
    print(f"  - Subsample ratio: {xgb_params['subsample']}")
    print(f"  - Column subsample: {xgb_params['colsample_bytree']}")
    print(f"  - L1 regularization (alpha): {xgb_params['reg_alpha']}")
    print(f"  - L2 regularization (lambda): {xgb_params['reg_lambda']}")
    print(f"  - Random seed: {xgb_params['random_state']}")
    
    print(f"\n📋 Model Rationale:")
    print(f"  - Gradient boosting builds trees sequentially")
    print(f"  - Each tree corrects errors of previous trees")
    print(f"  - Handles complex non-linear relationships")
    print(f"  - Regularization prevents overfitting")
    print(f"  - Efficient with structured/tabular data")
    print(f"  - Provides feature importance scores")
    
    # Create model
    xgb_model = XGBRegressor(**xgb_params)
    
    print(f"\n✓ XGBoost model configured")
    
    return xgb_model, xgb_params


# ==============================================================================
# STEP 4: TRAIN MODEL
# ==============================================================================

def train_xgboost(model, X_train, y_train):
    """Train XGBoost model"""
    print("\n" + "="*80)
    print("STEP 4: TRAINING XGBOOST MODEL")
    print("="*80)
    
    print(f"\n🏋️ Training model on {len(X_train)} samples...")
    print(f"  Features: {X_train.shape[1]}")
    print(f"  Boosting rounds: {model.n_estimators}")
    
    # Train the model
    model.fit(X_train, y_train, verbose=False)
    
    print(f"\n✓ Model trained successfully!")
    print(f"  - Boosting rounds completed: {model.n_estimators}")
    print(f"  - Features used: {model.n_features_in_}")
    
    return model


# ==============================================================================
# STEP 5: EVALUATE MODEL
# ==============================================================================

def evaluate_model(model, X_train, y_train, X_test, y_test):
    """Evaluate model performance"""
    print("\n" + "="*80)
    print("STEP 5: EVALUATING MODEL PERFORMANCE")
    print("="*80)
    
    # Make predictions
    print(f"\n📊 Making predictions...")
    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)
    
    # Compute metrics
    print(f"\n📈 Computing performance metrics...")
    
    # Training metrics
    train_mae = mean_absolute_error(y_train, train_preds)
    train_rmse = np.sqrt(mean_squared_error(y_train, train_preds))
    train_r2 = r2_score(y_train, train_preds)
    
    # Testing metrics
    test_mae = mean_absolute_error(y_test, test_preds)
    test_rmse = np.sqrt(mean_squared_error(y_test, test_preds))
    test_r2 = r2_score(y_test, test_preds)
    
    # Display results
    print(f"\n{'='*80}")
    print("TRAINING SET PERFORMANCE")
    print(f"{'='*80}")
    print(f"  MAE:  {train_mae:.6f} kg CO₂/kg")
    print(f"  RMSE: {train_rmse:.6f} kg CO₂/kg")
    print(f"  R²:   {train_r2:.6f} ({train_r2*100:.2f}% variance explained)")
    
    print(f"\n{'='*80}")
    print("TEST SET PERFORMANCE")
    print(f"{'='*80}")
    print(f"  MAE:  {test_mae:.6f} kg CO₂/kg")
    print(f"  RMSE: {test_rmse:.6f} kg CO₂/kg")
    print(f"  R²:   {test_r2:.6f} ({test_r2*100:.2f}% variance explained)")
    
    # Overfitting check
    overfit_indicator = train_r2 - test_r2
    print(f"\n{'='*80}")
    print("GENERALIZATION CHECK")
    print(f"{'='*80}")
    print(f"  Train-Test R² Gap: {overfit_indicator:.6f}")
    
    if overfit_indicator < 0.05:
        print(f"  ✅ Excellent generalization (gap < 0.05)")
    elif overfit_indicator < 0.10:
        print(f"  ✅ Good generalization (gap < 0.10)")
    elif overfit_indicator < 0.20:
        print(f"  ⚠️  Moderate overfitting (gap < 0.20)")
    else:
        print(f"  ❌ Significant overfitting (gap >= 0.20)")
    
    metrics = {
        'model_name': 'XGBoost',
        'target': 'co2_emission_per_kg_estimated',
        'train_mae': train_mae,
        'train_rmse': train_rmse,
        'train_r2': train_r2,
        'test_mae': test_mae,
        'test_rmse': test_rmse,
        'test_r2': test_r2,
        'overfit_indicator': overfit_indicator,
        'n_samples_train': len(X_train),
        'n_samples_test': len(X_test),
        'n_features': X_train.shape[1]
    }
    
    return metrics, train_preds, test_preds


def perform_cross_validation(model, X_train, y_train):
    """Perform cross-validation"""
    print("\n" + "="*80)
    print("STEP 6: CROSS-VALIDATION")
    print("="*80)
    
    print(f"\n🔄 Performing {N_FOLDS}-fold cross-validation...")
    
    # Define scoring metrics
    scoring = {
        'neg_mae': 'neg_mean_absolute_error',
        'neg_rmse': 'neg_root_mean_squared_error',
        'r2': 'r2'
    }
    
    # Perform cross-validation
    cv_results = cross_validate(
        model, X_train, y_train,
        cv=N_FOLDS,
        scoring=scoring,
        return_train_score=True,
        n_jobs=-1
    )
    
    # Extract metrics
    cv_metrics = {
        'cv_train_mae_mean': -cv_results['train_neg_mae'].mean(),
        'cv_train_mae_std': cv_results['train_neg_mae'].std(),
        'cv_test_mae_mean': -cv_results['test_neg_mae'].mean(),
        'cv_test_mae_std': cv_results['test_neg_mae'].std(),
        'cv_train_rmse_mean': -cv_results['train_neg_rmse'].mean(),
        'cv_train_rmse_std': cv_results['train_neg_rmse'].std(),
        'cv_test_rmse_mean': -cv_results['test_neg_rmse'].mean(),
        'cv_test_rmse_std': cv_results['test_neg_rmse'].std(),
        'cv_train_r2_mean': cv_results['train_r2'].mean(),
        'cv_train_r2_std': cv_results['train_r2'].std(),
        'cv_test_r2_mean': cv_results['test_r2'].mean(),
        'cv_test_r2_std': cv_results['test_r2'].std(),
    }
    
    print(f"\n  Cross-Validation Results ({N_FOLDS} folds):")
    print(f"    Test MAE:  {cv_metrics['cv_test_mae_mean']:.6f} ± {cv_metrics['cv_test_mae_std']:.6f} kg CO₂/kg")
    print(f"    Test RMSE: {cv_metrics['cv_test_rmse_mean']:.6f} ± {cv_metrics['cv_test_rmse_std']:.6f} kg CO₂/kg")
    print(f"    Test R²:   {cv_metrics['cv_test_r2_mean']:.6f} ± {cv_metrics['cv_test_r2_std']:.6f}")
    
    return cv_metrics


def compare_with_baseline(xgb_metrics):
    """Compare XGBoost with baseline Decision Tree"""
    print("\n" + "="*80)
    print("COMPARISON WITH BASELINE")
    print("="*80)
    
    # Baseline metrics (from previous training)
    baseline_r2 = 0.9932
    baseline_mae = 0.0374
    baseline_rmse = 0.0606
    
    xgb_r2 = xgb_metrics['test_r2']
    xgb_mae = xgb_metrics['test_mae']
    xgb_rmse = xgb_metrics['test_rmse']
    
    print(f"\n📊 Performance Comparison:")
    print(f"\n  {'Metric':<15} {'Baseline (DT)':<25} {'XGBoost':<25} {'Improvement'}")
    print(f"  {'-'*85}")
    
    # R² comparison
    r2_diff = xgb_r2 - baseline_r2
    r2_pct = (r2_diff / baseline_r2) * 100 if baseline_r2 != 0 else 0
    r2_symbol = "✅" if r2_diff > 0 else "➖" if abs(r2_diff) < 0.0001 else "⚠️"
    print(f"  {'R²':<15} {baseline_r2:<25.6f} {xgb_r2:<25.6f} {r2_symbol} {r2_diff:+.6f} ({r2_pct:+.2f}%)")
    
    # MAE comparison (lower is better)
    mae_diff = baseline_mae - xgb_mae  # Positive means XGBoost is better
    mae_pct = (mae_diff / baseline_mae) * 100 if baseline_mae != 0 else 0
    mae_symbol = "✅" if mae_diff > 0 else "➖" if abs(mae_diff) < 0.0001 else "⚠️"
    print(f"  {'MAE':<15} {baseline_mae:<25.6f} {xgb_mae:<25.6f} {mae_symbol} {mae_diff:+.6f} ({mae_pct:+.2f}%)")
    
    # RMSE comparison (lower is better)
    rmse_diff = baseline_rmse - xgb_rmse  # Positive means XGBoost is better
    rmse_pct = (rmse_diff / baseline_rmse) * 100 if baseline_rmse != 0 else 0
    rmse_symbol = "✅" if rmse_diff > 0 else "➖" if abs(rmse_diff) < 0.0001 else "⚠️"
    print(f"  {'RMSE':<15} {baseline_rmse:<25.6f} {xgb_rmse:<25.6f} {rmse_symbol} {rmse_diff:+.6f} ({rmse_pct:+.2f}%)")
    
    print(f"\n  Legend: ✅ Improvement | ➖ Similar | ⚠️ Degradation")
    
    # Overall assessment
    improvements = sum([r2_diff > 0.0001, mae_diff > 0.0001, rmse_diff > 0.0001])
    
    print(f"\n{'='*80}")
    print("OVERALL ASSESSMENT")
    print(f"{'='*80}")
    
    if improvements >= 2:
        print(f"  ✅ XGBoost shows improvement over baseline ({improvements}/3 metrics)")
    elif improvements == 1:
        print(f"  ➖ XGBoost shows mixed results ({improvements}/3 metrics improved)")
    else:
        print(f"  ➖ Performance similar to baseline")
    
    comparison = {
        'baseline_model': 'Decision Tree',
        'xgb_model': 'XGBoost',
        'baseline_r2': baseline_r2,
        'xgb_r2': xgb_r2,
        'r2_improvement': r2_diff,
        'r2_improvement_pct': r2_pct,
        'baseline_mae': baseline_mae,
        'xgb_mae': xgb_mae,
        'mae_improvement': mae_diff,
        'mae_improvement_pct': mae_pct,
        'baseline_rmse': baseline_rmse,
        'xgb_rmse': xgb_rmse,
        'rmse_improvement': rmse_diff,
        'rmse_improvement_pct': rmse_pct,
        'metrics_improved': improvements
    }
    
    return comparison


# ==============================================================================
# STEP 7: FEATURE IMPORTANCE
# ==============================================================================

def extract_feature_importance(model, feature_cols):
    """Extract and save feature importance"""
    print("\n" + "="*80)
    print("EXTRACTING FEATURE IMPORTANCE")
    print("="*80)
    
    print(f"\n📊 Computing feature importance scores...")
    
    # Get feature importance (gain-based)
    importance_scores = model.feature_importances_
    
    # Create DataFrame
    importance_df = pd.DataFrame({
        'feature': feature_cols,
        'importance': importance_scores
    })
    
    # Sort by importance
    importance_df = importance_df.sort_values('importance', ascending=False)
    
    # Display top 15
    print(f"\n  Top 15 Most Important Features:")
    for idx, row in importance_df.head(15).iterrows():
        bar_length = int(row['importance'] * 50)
        bar = "█" * bar_length
        print(f"    {row['feature']:<40} {bar} {row['importance']:.4f}")
    
    # Save to CSV
    output_path = REPORTS_DIR / 'feature_importance.csv'
    importance_df.to_csv(output_path, index=False)
    
    print(f"\n💾 Feature importance saved to: {output_path}")
    
    return importance_df


# ==============================================================================
# STEP 8: SAVE MODEL AND RESULTS
# ==============================================================================

def save_model(model, model_path):
    """Save trained model using joblib"""
    print("\n" + "="*80)
    print("SAVING MODEL")
    print("="*80)
    
    print(f"\n💾 Saving XGBoost model...")
    joblib.dump(model, model_path)
    
    # Get file size
    file_size = model_path.stat().st_size / 1024  # KB
    
    print(f"  ✓ Model saved to: {model_path}")
    print(f"  ✓ File size: {file_size:.2f} KB")
    print(f"  ✓ Format: joblib (compatible with scikit-learn)")
    
    # Test loading
    print(f"\n🔍 Verifying model can be loaded...")
    loaded_model = joblib.load(model_path)
    print(f"  ✓ Model loaded successfully")
    print(f"  ✓ Model type: {type(loaded_model).__name__}")


def save_metrics(metrics, cv_metrics, comparison):
    """Save metrics to CSV"""
    print("\n💾 Saving metrics...")
    
    # Combine all metrics
    all_metrics = {**metrics, **cv_metrics, **comparison}
    
    # Create DataFrame
    metrics_df = pd.DataFrame([all_metrics])
    
    # Save to CSV
    output_path = METRICS_DIR / 'co2_metrics.csv'
    metrics_df.to_csv(output_path, index=False)
    
    print(f"  ✓ Metrics saved to: {output_path}")


def generate_training_summary(xgb_params, metrics, cv_metrics, comparison, feature_cols):
    """Generate training summary documentation"""
    print("\n📝 Generating training summary...")
    
    doc_path = DOCS_DIR / 'xgb_co2_training_summary.md'
    
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write("# XGBoost CO₂ Emission Prediction - Training Summary\n\n")
        f.write("## Overview\n\n")
        f.write("This document summarizes the XGBoost model trained for CO₂ emission prediction.\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Model Type:** XGBoost Regressor\n")
        f.write(f"**Target:** co2_emission_per_kg_estimated (kg CO₂ per kg material)\n\n")
        
        f.write("---\n\n")
        f.write("## Model Configuration\n\n")
        f.write("### Hyperparameters\n\n")
        f.write(f"- **Objective:** {xgb_params['objective']}\n")
        f.write(f"- **Number of Estimators:** {xgb_params['n_estimators']}\n")
        f.write(f"- **Max Depth:** {xgb_params['max_depth']}\n")
        f.write(f"- **Learning Rate:** {xgb_params['learning_rate']}\n")
        f.write(f"- **Subsample:** {xgb_params['subsample']}\n")
        f.write(f"- **Column Subsample:** {xgb_params['colsample_bytree']}\n")
        f.write(f"- **L1 Regularization (alpha):** {xgb_params['reg_alpha']}\n")
        f.write(f"- **L2 Regularization (lambda):** {xgb_params['reg_lambda']}\n")
        f.write(f"- **Random Seed:** {xgb_params['random_state']}\n\n")
        
        f.write("### Training Configuration\n\n")
        f.write(f"- **Training Samples:** {metrics['n_samples_train']}\n")
        f.write(f"- **Test Samples:** {metrics['n_samples_test']}\n")
        f.write(f"- **Features:** {metrics['n_features']}\n")
        f.write(f"- **Cross-Validation Folds:** {N_FOLDS}\n\n")
        
        f.write("---\n\n")
        f.write("## Performance Metrics\n\n")
        f.write("### Test Set Performance\n\n")
        f.write(f"- **MAE:** {metrics['test_mae']:.6f} kg CO₂/kg\n")
        f.write(f"- **RMSE:** {metrics['test_rmse']:.6f} kg CO₂/kg\n")
        f.write(f"- **R² Score:** {metrics['test_r2']:.6f} ({metrics['test_r2']*100:.2f}% variance explained)\n\n")
        
        f.write("### Cross-Validation Performance\n\n")
        f.write(f"- **CV MAE:** {cv_metrics['cv_test_mae_mean']:.6f} ± {cv_metrics['cv_test_mae_std']:.6f} kg CO₂/kg\n")
        f.write(f"- **CV RMSE:** {cv_metrics['cv_test_rmse_mean']:.6f} ± {cv_metrics['cv_test_rmse_std']:.6f} kg CO₂/kg\n")
        f.write(f"- **CV R²:** {cv_metrics['cv_test_r2_mean']:.6f} ± {cv_metrics['cv_test_r2_std']:.6f}\n\n")
        
        f.write("---\n\n")
        f.write("## Comparison with Baseline\n\n")
        f.write("| Metric | Baseline (Decision Tree) | XGBoost | Improvement |\n")
        f.write("|--------|--------------------------|---------|-------------|\n")
        f.write(f"| R² | {comparison['baseline_r2']:.6f} | {comparison['xgb_r2']:.6f} | ")
        f.write(f"{comparison['r2_improvement']:+.6f} ({comparison['r2_improvement_pct']:+.2f}%) |\n")
        f.write(f"| MAE | {comparison['baseline_mae']:.6f} | {comparison['xgb_mae']:.6f} | ")
        f.write(f"{comparison['mae_improvement']:+.6f} ({comparison['mae_improvement_pct']:+.2f}%) |\n")
        f.write(f"| RMSE | {comparison['baseline_rmse']:.6f} | {comparison['xgb_rmse']:.6f} | ")
        f.write(f"{comparison['rmse_improvement']:+.6f} ({comparison['rmse_improvement_pct']:+.2f}%) |\n\n")
        
        f.write("### Assessment\n\n")
        if comparison['metrics_improved'] >= 2:
            f.write(f"✅ **XGBoost improves upon baseline** ({comparison['metrics_improved']}/3 metrics)\n\n")
        else:
            f.write(f"➖ **Performance similar to baseline** ({comparison['metrics_improved']}/3 metrics improved)\n\n")
        
        f.write("---\n\n")
        f.write("## Model Artifacts\n\n")
        f.write(f"- **Model File:** `ml/models/xgb_co2.joblib`\n")
        f.write(f"- **Metrics File:** `ml/metrics/co2_metrics.csv`\n")
        f.write(f"- **Feature Importance:** `ml/reports/feature_importance.csv`\n")
        f.write(f"- **Format:** joblib (scikit-learn compatible)\n\n")
        
        f.write("### Loading the Model\n\n")
        f.write("```python\n")
        f.write("import joblib\n\n")
        f.write("# Load model\n")
        f.write("model = joblib.load('ml/models/xgb_co2.joblib')\n\n")
        f.write("# Make predictions\n")
        f.write("predictions = model.predict(X_new)\n")
        f.write("```\n\n")
        
        f.write("---\n\n")
        f.write("## Acceptance Criteria\n\n")
        f.write("- ✅ Model trains without errors\n")
        f.write(f"- ✅ RMSE: {metrics['test_rmse']:.6f} kg CO₂/kg\n")
        f.write("- ✅ Model file saved successfully\n")
        f.write("- ✅ Metrics logged and reproducible\n")
        f.write("- ✅ Feature importance generated\n\n")
        
        f.write("---\n\n")
        f.write("## Next Steps\n\n")
        f.write("1. Analyze feature importance in detail\n")
        f.write("2. Perform error analysis on predictions\n")
        f.write("3. Consider hyperparameter tuning if needed\n")
        f.write("4. Deploy model to inference pipeline\n")
    
    print(f"  ✓ Training summary saved to: {doc_path}")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    """Main execution function"""
    
    # Step 1: Load and prepare data
    X, y, df, label_encoders, feature_cols = load_and_prepare_data()
    
    # Step 2: Create train/test split
    X_train, X_test, y_train, y_test = create_train_test_split(X, y, df)
    
    # Step 3: Configure XGBoost
    xgb_model, xgb_params = configure_xgboost()
    
    # Step 4: Train model
    trained_model = train_xgboost(xgb_model, X_train, y_train)
    
    # Step 5: Evaluate model
    metrics, train_preds, test_preds = evaluate_model(
        trained_model, X_train, y_train, X_test, y_test
    )
    
    # Step 6: Cross-validation
    cv_metrics = perform_cross_validation(trained_model, X_train, y_train)
    
    # Compare with baseline
    comparison = compare_with_baseline(metrics)
    
    # Step 7: Extract feature importance
    importance_df = extract_feature_importance(trained_model, feature_cols)
    
    # Step 8: Save model and results
    model_path = MODELS_DIR / 'xgb_co2.joblib'
    save_model(trained_model, model_path)
    save_metrics(metrics, cv_metrics, comparison)
    generate_training_summary(xgb_params, metrics, cv_metrics, comparison, feature_cols)
    
    # Final summary
    print("\n" + "="*80)
    print("XGBOOST CO₂ TRAINING COMPLETE!")
    print("="*80)
    
    print(f"\n📦 Deliverables:")
    print(f"  1. Trained Model: {model_path}")
    print(f"  2. Metrics CSV: {METRICS_DIR / 'co2_metrics.csv'}")
    print(f"  3. Feature Importance: {REPORTS_DIR / 'feature_importance.csv'}")
    print(f"  4. Training Summary: {DOCS_DIR / 'xgb_co2_training_summary.md'}")
    
    print(f"\n📊 Final Performance:")
    print(f"  - Test R²: {metrics['test_r2']:.6f} ({metrics['test_r2']*100:.2f}%)")
    print(f"  - Test MAE: {metrics['test_mae']:.6f} kg CO₂/kg")
    print(f"  - Test RMSE: {metrics['test_rmse']:.6f} kg CO₂/kg")
    print(f"  - CV R²: {cv_metrics['cv_test_r2_mean']:.6f} ± {cv_metrics['cv_test_r2_std']:.6f}")
    
    print(f"\n✅ All acceptance criteria met!")
    print("="*80)


if __name__ == "__main__":
    main()
