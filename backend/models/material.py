from backend.db import db

class Material(db.Model):
    __tablename__ = 'materials'

    material_id = db.Column(db.Integer, primary_key=True)
    material_type = db.Column(db.String(100), nullable=False)
    strength_mpa = db.Column(db.Numeric(10, 2))
    weight_capacity = db.Column(db.Numeric(10, 2))
    biodegradability_percent = db.Column(db.Numeric(5, 2))
    co2_emission_score = db.Column(db.Numeric(10, 2))
    recyclability_percent = db.Column(db.Numeric(5, 2))
    cost_per_kg = db.Column(db.Numeric(10, 2))
    industry_use_case = db.Column(db.String(200))

    def to_dict(self):
        return {
            'material_id': self.material_id,
            'material_type': self.material_type,
            'strength_mpa': float(self.strength_mpa) if self.strength_mpa else None,
            'weight_capacity': float(self.weight_capacity) if self.weight_capacity else None,
            'biodegradability_percent': float(self.biodegradability_percent) if self.biodegradability_percent else None,
            'co2_emission_score': float(self.co2_emission_score) if self.co2_emission_score else None,
            'recyclability_percent': float(self.recyclability_percent) if self.recyclability_percent else None,
            'cost_per_kg': float(self.cost_per_kg) if self.cost_per_kg else None,
            'industry_use_case': self.industry_use_case
        }
