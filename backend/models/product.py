from backend.db import db

class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    product_weight = db.Column(db.Numeric(10, 2))
    fragility_index = db.Column(db.Integer)
    shipping_type = db.Column(db.String(50))

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'category': self.category,
            'product_weight': float(self.product_weight) if self.product_weight else None,
            'fragility_index': self.fragility_index,
            'shipping_type': self.shipping_type
        }
