from api.extensions import db

class Material(db.Model):
    __tablename__ = "materials"

    material_id = db.Column(db.Integer, primary_key=True)

    material_type = db.Column(db.String(100), nullable=False)
    strength_mpa = db.Column(db.Float)
    weight_capacity = db.Column(db.Float)
    recyclability_percent = db.Column(db.Float)
    biodegradability_percent = db.Column(db.Float)
    cost_per_kg = db.Column(db.Float)
