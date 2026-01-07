from . import db

class Material(db.Model):
    __tablename__ = "materials"

    material_id = db.Column(db.Integer, primary_key=True)
    material_type = db.Column(db.String(100), nullable=False)
    recyclability_percent = db.Column(db.Float)
    co2_emission_score = db.Column(db.Float)
    cost_per_kg = db.Column(db.Float)
