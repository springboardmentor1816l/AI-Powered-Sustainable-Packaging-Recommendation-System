"""
Recommendation Log Model
========================

SQLAlchemy model for recommendation logs.

Author: EcoPackAI Team
Date: 2026-01-03
"""

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import db

class RecommendationLog(db.Model):
    """
    Recommendation Log model - stores ML model prediction results
    
    Attributes:
        rec_id: Primary key
        product_id: Foreign key to products table
        recommended_material_id: Foreign key to materials table
        cost_prediction: Predicted cost
        co2_prediction: Predicted CO₂ emissions
        material_rank: Ranking of material (1 = best match)
        confidence_score: ML model confidence score (0-1)
        created_at: Timestamp when prediction was logged
    """
    
    __tablename__ = 'recommendation_logs'
    
    rec_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(
        Integer,
        ForeignKey('products.product_id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    recommended_material_id = Column(
        Integer,
        ForeignKey('materials.material_id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    cost_prediction = Column(Float)
    co2_prediction = Column(Float)
    material_rank = Column(Integer, CheckConstraint('material_rank >= 1'))
    confidence_score = Column(
        Float,
        CheckConstraint('confidence_score >= 0 AND confidence_score <= 1')
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    product = relationship('Product', back_populates='recommendations')
    material = relationship('Material', back_populates='recommendations')
    
    def __repr__(self):
        return f"<RecommendationLog(id={self.rec_id}, product_id={self.product_id}, material_id={self.recommended_material_id})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'rec_id': self.rec_id,
            'product_id': self.product_id,
            'recommended_material_id': self.recommended_material_id,
            'cost_prediction': self.cost_prediction,
            'co2_prediction': self.co2_prediction,
            'material_rank': self.material_rank,
            'confidence_score': self.confidence_score,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def from_prediction(cls, product_id, material_id, predictions, rank=1, confidence=None):
        """
        Create log from prediction results
        
        Args:
            product_id: Product ID
            material_id: Material ID
            predictions: Dictionary with cost and CO₂ predictions
            rank: Material ranking (default: 1)
            confidence: Confidence score (optional)
            
        Returns:
            RecommendationLog instance
        """
        return cls(
            product_id=product_id,
            recommended_material_id=material_id,
            cost_prediction=predictions.get('predicted_cost'),
            co2_prediction=predictions.get('predicted_co2'),
            material_rank=rank,
            confidence_score=confidence or predictions.get('cost_confidence')
        )
