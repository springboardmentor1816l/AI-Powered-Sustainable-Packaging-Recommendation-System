from src.db.database import db

class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    product_weight = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    fragility_index = db.Column(db.Float)
