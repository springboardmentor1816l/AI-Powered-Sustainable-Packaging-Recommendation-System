from api.extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    product_name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=False)

    fragility_index = db.Column(db.Integer, nullable=False)

    material_id = db.Column(
        db.Integer,
        db.ForeignKey("materials.id"),
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    material = db.relationship("Material", backref="products")

    def __repr__(self):
        return f"<Product {self.product_name}>"
