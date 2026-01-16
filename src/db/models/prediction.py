from src.db.database import db
from datetime import datetime

class Prediction(db.Model):
    __tablename__ = "prediction"

    id = db.Column(db.Integer, primary_key=True)
    predicted_cost = db.Column(db.Float, nullable=False)
    predicted_co2 = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
