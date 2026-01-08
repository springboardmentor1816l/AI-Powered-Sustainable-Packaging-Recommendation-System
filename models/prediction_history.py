from app import db

class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_data = db.Column(db.String(255))
    output_data = db.Column(db.String(255))
