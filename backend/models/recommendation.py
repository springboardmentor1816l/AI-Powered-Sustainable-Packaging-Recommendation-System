from backend.extensions import db
from datetime import datetime

class Recommendation(db.Model):
    __tablename__ = "recommendation"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    material_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
