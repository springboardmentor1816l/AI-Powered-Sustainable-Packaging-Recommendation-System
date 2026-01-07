from app import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(100))
    weight_kg = db.Column(db.Float)
    fragility_index = db.Column(db.Integer)

    material_id = db.Column(
        db.Integer,
        db.ForeignKey("materials.id"),
        nullable=False
    )

    predictions = db.relationship("Prediction", backref="product", lazy=True)
