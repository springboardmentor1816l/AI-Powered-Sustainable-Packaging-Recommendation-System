from api.extensions import db
from datetime import datetime

class PredictionHistory(db.Model):
    __tablename__ = "prediction_history"

    id = db.Column(db.Integer, primary_key=True)

    request_payload = db.Column(db.JSON, nullable=False)
    response_payload = db.Column(db.JSON, nullable=False)

    status = db.Column(db.String(50), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PredictionHistory {self.status}>"
