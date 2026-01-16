from src.db.database import db

class Material(db.Model):
    __tablename__ = "material"

    id = db.Column(db.Integer, primary_key=True)
    material_type = db.Column(db.String(50), nullable=False)
    recyclability_score = db.Column(db.Float)
