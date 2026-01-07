from backend.extensions import db


class PredictionHistory(db.Model):
    __tablename__ = "prediction_history"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    predicted_cost = db.Column(db.Float, nullable=False)
    predicted_co2 = db.Column(db.Float, nullable=False)
    model_version = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
