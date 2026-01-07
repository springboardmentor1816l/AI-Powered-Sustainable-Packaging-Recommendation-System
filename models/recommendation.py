from extensions import db

class Recommendation(db.Model):
    __tablename__ = "recommendations"

    id = db.Column(db.Integer, primary_key=True)
    material_type = db.Column(db.String(100))
    weight_capacity = db.Column(db.Float)
    sustainability_score = db.Column(db.Float)

    prediction_id = db.Column(
        db.Integer,
        db.ForeignKey("predictions.id"),
        nullable=False
    )
