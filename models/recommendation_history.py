from sqlalchemy import Column, Integer, JSON, DateTime
from datetime import datetime
from .db import Base

class RecommendationHistory(Base):
    __tablename__ = "recommendation_history"

    id = Column(Integer, primary_key=True)
    input_payload = Column(JSON, nullable=False)
    ranked_output = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
