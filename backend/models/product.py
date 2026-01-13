from . import db

class Product(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    product_weight = db.Column(db.Float)
    fragility_index = db.Column(db.Integer)
    shipping_type = db.Column(db.String(50))
