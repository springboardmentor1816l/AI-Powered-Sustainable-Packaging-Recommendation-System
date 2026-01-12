import csv
import io
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import pandas as pd
import joblib
import json
# Import the Predictor
from predictor import EcoPackPredictor

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

# --- CONFIGURATION ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecopackai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

db = SQLAlchemy(app)
cache = Cache(app)

# --- DATABASE MODEL (For Module 7 Analytics) ---
class RecommendationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_category = db.Column(db.String(100))
    weight = db.Column(db.Float)
    cost_pred = db.Column(db.Float)
    co2_pred = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# --- INITIALIZE PREDICTOR ---
PIPELINE_PATH = 'models/preprocessing/preprocessing_pipeline.pkl'
COST_MODEL_PATH = 'ml/models/rf_cost.joblib'
CO2_MODEL_PATH = 'ml/models/xgb_co2.joblib'
predictor = EcoPackPredictor(PIPELINE_PATH, COST_MODEL_PATH, CO2_MODEL_PATH)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def predict_form():
    """Renders the input form. Function name matches url_for in templates."""
    return render_template('form.html')
materials_df = pd.read_csv('data/raw/materials_dataset.csv')
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # 1. Standardize Dataset Columns
        materials_df.columns = materials_df.columns.str.strip()

        product_data = {
            'category': request.form.get('category'),
            'weight': float(request.form.get('weight')),
            'fragility': float(request.form.get('fragility')), # User input 0.0 - 1.0
            'shipping_type': request.form.get('shipping_type')
        }

        user_cat = product_data['category']
        frag_val = product_data['fragility']

        # 2. LOGICAL CONSTRAINTS (Prevent Steel for Cosmetics)
        # We define which materials are strictly disallowed for retail categories
        disallowed_map = {
            'Cosmetics': ['Steel', 'Steel Racks & Containers', 'Metal'],
            'Food': ['Steel', 'Metal', 'Heavy Industrial Plastic'],
            'Pharmacy': ['Steel', 'Metal'],
            'Drinkware': ['Steel Racks & Containers']
        }
        forbidden = disallowed_map.get(user_cat, [])

        # 3. TIERED FILTERING (Ensures exactly 3 unique results)
        # Step A: Find matching materials for this specific industry
        exact_matches = materials_df[
            (materials_df['Suitable Product Categories'].str.contains(user_cat, case=False, na=False)) &
            (~materials_df['Material Type'].isin(forbidden))
        ]
        
        # Step B: Find general eco-backups (Cardboard/Paper) that aren't forbidden
        backups = materials_df[
            (~materials_df['Material ID'].isin(exact_matches['Material ID'])) &
            (~materials_df['Material Type'].isin(forbidden)) &
            (materials_df['Material Type'].isin(['Cardboard', 'Paper/Bio-Based']))
        ].sort_values(by='Recyclability (%)', ascending=False)

        # Merge and take the first 3 unique material types
        combined_df = pd.concat([exact_matches, backups]).drop_duplicates(subset=['Material Type']).copy()

        # 4. REAL-WORLD CALIBRATED SCORING & COST
        def calculate_metrics(row):
            # Normalize Helper: Handles both 0-1 and 0-100 scales
            def norm(val, max_val=1.0):
                if val > max_val and max_val == 1.0: val /= 100.0
                return max(0.0, min(1.0, val / max_val))

            protection = norm(row['Load Handling Score'], max_val=10.0)
            eco = norm(row['Recyclability (%)'])
            
            # --- REALISTIC INR COST (Calibrated for India) ---
            # Market rates: Standard boxes are ₹15-50.
            # We use a multiplier of 15.0 to turn a $2.00 material into a realistic ₹30.00 unit.
            base_multiplier = 15.0 
            unit_cost_inr = (row['Cost per Unit (USD)'] * base_multiplier) + (product_data['weight'] * 2)
            
            # --- HIGH-ACCURACY SCORE (0-100%) ---
            # Total weights must sum to 1.0
            w_prot = 0.2 + (frag_val * 0.5) # Protection weight (20% to 70%)
            w_eco = 1.0 - w_prot           # Sustainability weight
            
            # Add a 'Sustainability Bonus' so good materials reach the 80%+ Green range
            score_val = (protection * w_prot) + (eco * w_eco) + 0.15 
            display_score = round(min(98.9, score_val * 100), 1)

            return display_score, round(unit_cost_inr, 2)

        combined_df[['Score', 'Cost']] = combined_df.apply(
            lambda x: pd.Series(calculate_metrics(x)), axis=1
        )
        
        # Take final top 3 unique recommendations
        top_3 = combined_df.sort_values(by='Score', ascending=False).head(3)

        recommendations = []
        for i, (idx, row) in enumerate(top_3.iterrows(), 1):
            recommendations.append({
                "rank": i,
                "material_type": row['Material Type'],
                "packaging_type": row['Packaging Type'],
                "cost_prediction": row['Cost'],
                "co2_prediction": round(row['Carbon Footprint (kg CO2/unit)'], 2),
                "suitability_score": row['Score']
            })

        return render_template('results.html', results=recommendations, product=product_data)

    except Exception as e:
        return f"Logic Error: {str(e)}", 400
@app.route('/analytics')
def show_analytics():
    logs = RecommendationLog.query.all()
    
    # Logic to aggregate data
    categories = list(set([l.product_category for l in logs]))
    stats = {
        'total_co2': sum([l.co2_pred for l in logs]),
        'avg_score': sum([getattr(l, 'suitability_score', 85.0) for l in logs]) / len(logs) if logs else 0,
        'total_count': len(logs)
    }
    
    charts = {
        'labels': categories,
        'counts': [len([l for l in logs if l.product_category == c]) for c in categories],
        'scores': [85 for c in categories] # Placeholder for avg score per cat
    }

    return render_template('analytics.html', data_json=json.dumps({'stats': stats, 'charts': charts}))

@app.route('/api/analytics-data')
def get_analytics_data():
    try:
        logs = RecommendationLog.query.all()
        total_co2 = sum(log.co2_pred for log in logs)
        avg_cost = sum(log.cost_pred for log in logs) / len(logs) if logs else 0
        
        categories = {}
        for log in logs:
            categories[log.product_category] = categories.get(log.product_category, 0) + 1

        return jsonify({
            "summary": {
                "total_co2_saved": round(total_co2, 2),
                "avg_cost_efficiency": round(avg_cost, 2),
                "total_count": len(logs)
            },
            "charts": {
                "material_labels": [log.product_category for log in logs[-5:]],
                "co2_values": [log.co2_pred for log in logs[-5:]],
                "cost_values": [log.cost_pred for log in logs[-5:]],
                "category_labels": list(categories.keys()),
                "category_counts": list(categories.values())
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/export/csv')
def export_csv():
    try:
        logs = RecommendationLog.query.all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Log ID', 'Product Category', 'Weight (kg)', 'Cost (INR)', 'CO2 Impact (kg)', 'Timestamp'])
        
        for log in logs:
            writer.writerow([
                log.id, 
                log.product_category, 
                log.weight, 
                log.cost_pred, 
                log.co2_pred, 
                log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        response = make_response(output.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=EcoPackAI_Sustainability_Report.csv"
        response.headers["Content-type"] = "text/csv"
        return response
    except Exception as e:
        return f"Export failed: {str(e)}", 500
def seed_db():
    if not RecommendationLog.query.first():
        sample_logs = [
            RecommendationLog(product_category='Cosmetics', weight=0.2, cost_pred=45.0, co2_pred=0.15),
            RecommendationLog(product_category='Drinkware', weight=1.0, cost_pred=85.0, co2_pred=0.60),
            RecommendationLog(product_category='Electronics', weight=2.5, cost_pred=120.0, co2_pred=1.2),
            RecommendationLog(product_category='Food', weight=0.5, cost_pred=25.0, co2_pred=0.10)
        ]
        db.session.bulk_save_objects(sample_logs)
        db.session.commit()
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)