from . import db
from datetime import datetime


class Prediction(db.Model):
    __tablename__ = "recommendation_logs"

    rec_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    recommended_material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'))
    cost_prediction = db.Column(db.Float)
    co2_prediction = db.Column(db.Float)
    material_rank = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
