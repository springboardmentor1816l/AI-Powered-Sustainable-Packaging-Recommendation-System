from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 1. MATERIALS MODEL - Holds the library of available materials
class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    material_name = db.Column(db.String(100), nullable=False)
    material_type = db.Column(db.String(50)) # Matches 'Material Type_...' from OHE
    cost_per_kg = db.Column(db.Float)
    carbon_footprint = db.Column(db.Float)
    recyclability_pct = db.Column(db.Float) # Matches 'Recyclability (%)'

# 2. PRODUCTS MODEL - Holds the product being analyzed
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50)) # Matches 'category_...' from OHE
    product_weight_kg = db.Column(db.Float) # Exact match to preprocessing
    fragility_index = db.Column(db.Float)   # Exact match to preprocessing
    
    # Links to history
    predictions = db.relationship('PredictionHistory', backref='product', lazy=True)

# 3. PREDICTION HISTORY - Stores the results of the model
class PredictionHistory(db.Model):
    __tablename__ = 'prediction_history'
    id = db.Column(db.Integer, primary_key=True)
    # Changed nullable to True so predictions don't fail without a product record
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    
    # ADD THESE COLUMNS to match your API input exactly
    product_weight_kg = db.Column(db.Float) 
    category = db.Column(db.String(50))
    
    # Target columns
    predicted_cost_index = db.Column(db.Float) 
    predicted_co2_impact = db.Column(db.Float)
    
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)