from extensions.db import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    fragile = db.Column(db.Boolean, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
