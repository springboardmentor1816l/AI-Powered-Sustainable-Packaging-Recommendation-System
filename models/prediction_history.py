from sqlalchemy import Column, Integer, Float, DateTime, JSON
from datetime import datetime
from .db import Base

class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True)
    request_payload = Column(JSON, nullable=False)
    predicted_cost = Column(Float, nullable=False)
    predicted_co2 = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
