"""
EcoPackAI - Database Models (SQLAlchemy ORM)
Module: Backend - Database Integration
Output: Database schema definitions
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ============================================
# MATERIALS TABLE
# ============================================
class Material(db.Model):
    __tablename__ = 'materials'
    
    material_id = db.Column(db.Integer, primary_key=True)
    material_type = db.Column(db.String(100), nullable=False)
    packaging_type = db.Column(db.String(100), nullable=False)
    
    # Physical properties
    strength_mpa = db.Column(db.Float)
    weight_capacity = db.Column(db.Float)
    load_handling_score = db.Column(db.Integer)
    moisture_resistance = db.Column(db.Integer)
    thermal_resistance = db.Column(db.Integer)
    
    # Sustainability metrics
    biodegradability_percent = db.Column(db.Float)
    recyclability_percent = db.Column(db.Float)
    recycled_content_percent = db.Column(db.Float)
    reusability_percent = db.Column(db.Float)
    biodegradation_days = db.Column(db.Float)
    
    # Environmental impact
    co2_emission_score = db.Column(db.Float)
    carbon_footprint = db.Column(db.Float)
    waste_reduction_impact = db.Column(db.Float)
    
    # Cost
    cost_per_kg = db.Column(db.Float)
    cost_per_unit_usd = db.Column(db.Float)
    
    # Other
    supplier_region = db.Column(db.String(50))
    industry_use_case = db.Column(db.String(200))
    suitable_categories = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recommendations = db.relationship('Recommendation', backref='material', lazy=True)
    
    def to_dict(self):
        return {
            'material_id': self.material_id,
            'material_type': self.material_type,
            'packaging_type': self.packaging_type,
            'recyclability_percent': self.recyclability_percent,
            'cost_per_unit_usd': self.cost_per_unit_usd,
            'co2_emission_score': self.co2_emission_score
        }


# ============================================
# PRODUCTS TABLE
# ============================================
class Product(db.Model):
    __tablename__ = 'products'
    
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    
    # Physical attributes
    product_weight = db.Column(db.Float)
    fragility_index = db.Column(db.Integer)
    shipping_type = db.Column(db.String(50))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recommendations = db.relationship('Recommendation', backref='product', lazy=True)
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'category': self.category,
            'product_weight': self.product_weight,
            'fragility_index': self.fragility_index,
            'shipping_type': self.shipping_type
        }


# ============================================
# RECOMMENDATIONS TABLE
# ============================================
class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    rec_id = db.Column(db.Integer, primary_key=True)
    
    # Foreign keys
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'), nullable=False)
    
    # Predictions
    cost_prediction = db.Column(db.Float)
    co2_prediction = db.Column(db.Float)
    suitability_score = db.Column(db.Float)
    composite_score = db.Column(db.Float)
    material_rank = db.Column(db.Integer)
    
    # Metadata
    model_version = db.Column(db.String(20))
    prediction_time = db.Column(db.Float)  # milliseconds
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'rec_id': self.rec_id,
            'product_id': self.product_id,
            'material_id': self.material_id,
            'cost_prediction': self.cost_prediction,
            'co2_prediction': self.co2_prediction,
            'suitability_score': self.suitability_score,
            'material_rank': self.material_rank,
            'created_at': self.created_at.isoformat()
        }


# ============================================
# PREDICTION HISTORY TABLE
# ============================================
class PredictionHistory(db.Model):
    __tablename__ = 'prediction_history'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Request data
    request_data = db.Column(db.JSON)
    
    # Response data
    predictions = db.Column(db.JSON)
    
    # Metadata
    user_ip = db.Column(db.String(50))
    user_agent = db.Column(db.String(200))
    response_time_ms = db.Column(db.Float)
    status_code = db.Column(db.Integer)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'request_data': self.request_data,
            'predictions': self.predictions,
            'created_at': self.created_at.isoformat()
        }


# ============================================
# API KEYS TABLE (for authentication)
# ============================================
class APIKey(db.Model):
    __tablename__ = 'api_keys'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    
    # Usage tracking
    request_count = db.Column(db.Integer, default=0)
    last_used = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'is_active': self.is_active,
            'request_count': self.request_count,
            'created_at': self.created_at.isoformat()
        }


# ============================================
# DATABASE INITIALIZATION FUNCTIONS
# ============================================
def init_db(app):
    """Initialize database with app context"""
    try:
        db.init_app(app)
        with app.app_context():
            db.create_all()
            print("✓ Database tables created")
    except RuntimeError as e:
        if "already been registered" in str(e):
            # Database already initialized, just create tables
            with app.app_context():
                db.create_all()
                print("✓ Database tables created")
        else:
            raise


def seed_database():
    """Seed database with sample data"""
    # Check if data already exists
    if Material.query.first():
        print("Database already seeded")
        return
    
    # Add sample materials
    materials = [
        Material(
            material_type="Cardboard",
            packaging_type="Cardboard Boxes",
            recyclability_percent=98,
            biodegradation_days=188,
            cost_per_unit_usd=2.24,
            co2_emission_score=0.54,
            load_handling_score=6,
            moisture_resistance=5,
            thermal_resistance=4
        ),
        Material(
            material_type="Paper/Bio-Based",
            packaging_type="Protective Fillers",
            recyclability_percent=100,
            biodegradation_days=65,
            cost_per_unit_usd=1.82,
            co2_emission_score=0.32,
            load_handling_score=3,
            moisture_resistance=3,
            thermal_resistance=3
        )
    ]
    
    # Add sample products
    products = [
        Product(
            product_name="Chocolate Box",
            category="Food",
            product_weight=0.5,
            fragility_index=2,
            shipping_type="Air"
        ),
        Product(
            product_name="Smartphone",
            category="Electronics",
            product_weight=0.3,
            fragility_index=5,
            shipping_type="Air"
        )
    ]
    
    db.session.add_all(materials)
    db.session.add_all(products)
    db.session.commit()
    
    print("✓ Database seeded with sample data")