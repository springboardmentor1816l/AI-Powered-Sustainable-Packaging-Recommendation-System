from models.db import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    weight = db.Column(db.Float)
    category = db.Column(db.String(50))

