from api.extensions import db
from datetime import datetime

class Material(db.Model):
    __tablename__ = "materials"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    biodegradability_percent = db.Column(db.Float, nullable=False)
    co2_per_kg = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Material {self.name}>"
