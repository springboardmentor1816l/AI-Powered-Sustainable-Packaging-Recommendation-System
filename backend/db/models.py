from datetime import datetime
from backend.db.base import db
class Material(db.Model):
    __tablename__ = "materials"

    id = db.Column(db.Integer, primary_key=True)

    material_type = db.Column(db.String(50), nullable=False)
    source_type = db.Column(db.String(50), nullable=False)
    recyclability_category = db.Column(db.String(50), nullable=False)

    recyclability_percent = db.Column(db.Float, nullable=False)
    biodegradability_percent = db.Column(db.Float, nullable=False)
    strength_mpa = db.Column(db.Float, nullable=False)

    co2_emission_kg_per_kg = db.Column(db.Float, nullable=False)
    co2_impact_index = db.Column(db.Float, nullable=False)
    cost_efficiency_index = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    industry_use_case = db.Column(db.String(50), nullable=False)
    weight_capacity_kg = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    predicted_score = db.Column(db.Float, nullable=False)
    model_version = db.Column(db.String(20), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship("Product", backref="predictions")
class Recommendation(db.Model):
    __tablename__ = "recommendations"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    material_id = db.Column(
        db.Integer,
        db.ForeignKey("materials.id"),
        nullable=False
    )

    rank = db.Column(db.Integer, nullable=False)
    final_score = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship("Product", backref="recommendations")
    material = db.relationship("Material", backref="recommendations")
