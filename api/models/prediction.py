from api.extensions import db
from datetime import datetime

class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    predicted_co2 = db.Column(db.Float, nullable=False)
    predicted_cost = db.Column(db.Float, nullable=False)

    recommendation_score = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    product = db.relationship("Product", backref="predictions")

    def __repr__(self):
        return f"<Prediction product_id={self.product_id}>"
