from backend.db import db
from datetime import datetime

class RecommendationLog(db.Model):
    __tablename__ = 'recommendation_logs'

    rec_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id', ondelete='CASCADE'))
    recommended_material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id', ondelete='SET NULL'))
    cost_prediction = db.Column(db.Numeric(10, 2))
    co2_prediction = db.Column(db.Numeric(10, 2))
    material_rank = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', backref=db.backref('recommendations', lazy=True))
    material = db.relationship('Material', backref=db.backref('recommendations', lazy=True))

    def to_dict(self):
        return {
            'rec_id': self.rec_id,
            'product_id': self.product_id,
            'recommended_material_id': self.recommended_material_id,
            'cost_prediction': float(self.cost_prediction) if self.cost_prediction else None,
            'co2_prediction': float(self.co2_prediction) if self.co2_prediction else None,
            'material_rank': self.material_rank,
            'created_at': self.created_at.isoformat()
        }
