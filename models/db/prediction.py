from extensions.db import db

class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    material_id = db.Column(db.Integer, db.ForeignKey("materials.id"))

    predicted_cost = db.Column(db.Float)
    predicted_co2 = db.Column(db.Float)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
