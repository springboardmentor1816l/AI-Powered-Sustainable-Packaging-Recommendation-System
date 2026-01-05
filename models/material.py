from models.db import db

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    recyclable = db.Column(db.Boolean)
    co2_factor = db.Column(db.Float)

