from . import db
from datetime import datetime


class Prediction(db.Model):
    __tablename__ = "recommendation_logs"

    rec_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    material_id = db.Column(db.Integer)
    predicted_cost = db.Column(db.Float)
    predicted_co2 = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
