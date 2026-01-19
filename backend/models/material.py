"""
Material Model
==============

SQLAlchemy model for packaging materials.

Author: EcoPackAI Team
Date: 2026-01-03
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import db

class Material(db.Model):
    """
    Material model - stores eco-friendly packaging material information
    
    Attributes:
        material_id: Primary key
        material_type: Name/type of packaging material
        strength_mpa: Mechanical strength in MegaPascals
        weight_capacity: Maximum load capacity in kg
        biodegradability_percent: Biodegradability percentage
        co2_emission_score: Carbon footprint index
        recyclability_percent: Recyclability percentage
        cost_per_kg: Cost per kilogram
        industry_use_case: Primary industries using this material
        created_at: Record creation timestamp
        updated_at: Record last update timestamp
    """
    
    __tablename__ = 'materials'
    
    material_id = Column(Integer, primary_key=True, autoincrement=True)
    material_type = Column(String(100), nullable=False, index=True)
    strength_mpa = Column(Float, CheckConstraint('strength_mpa >= 0'))
    weight_capacity = Column(Float, CheckConstraint('weight_capacity >= 0'))
    biodegradability_percent = Column(
        Float,
        CheckConstraint('biodegradability_percent >= 0 AND biodegradability_percent <= 100')
    )
    co2_emission_score = Column(Float, CheckConstraint('co2_emission_score >= 0'))
    recyclability_percent = Column(
        Float,
        CheckConstraint('recyclability_percent >= 0 AND recyclability_percent <= 100')
    )
    cost_per_kg = Column(Float, CheckConstraint('cost_per_kg >= 0'))
    industry_use_case = Column(String(200), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    recommendations = relationship('RecommendationLog', back_populates='material', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Material(id={self.material_id}, type='{self.material_type}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'material_id': self.material_id,
            'material_type': self.material_type,
            'strength_mpa': self.strength_mpa,
            'weight_capacity': self.weight_capacity,
            'biodegradability_percent': self.biodegradability_percent,
            'co2_emission_score': self.co2_emission_score,
            'recyclability_percent': self.recyclability_percent,
            'cost_per_kg': self.cost_per_kg,
            'industry_use_case': self.industry_use_case,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create model instance from dictionary"""
        return cls(
            material_type=data.get('material_type'),
            strength_mpa=data.get('strength_mpa'),
            weight_capacity=data.get('weight_capacity'),
            biodegradability_percent=data.get('biodegradability_percent'),
            co2_emission_score=data.get('co2_emission_score'),
            recyclability_percent=data.get('recyclability_percent'),
            cost_per_kg=data.get('cost_per_kg'),
            industry_use_case=data.get('industry_use_case')
        )
