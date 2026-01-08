from extensions.db import db

class Material(db.Model):
    __tablename__ = "materials"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    recyclable = db.Column(db.Boolean, nullable=False)
    co2_factor = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
