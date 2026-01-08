from app import db

class RecommendationResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    recommended_material = db.Column(db.String(100))
    score = db.Column(db.Float)
