"""
Product Model
=============

SQLAlchemy model for products.

Author: EcoPackAI Team
Date: 2026-01-03
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import db

class Product(db.Model):
    """
    Product model - stores product-specific attributes for packaging recommendation
    
    Attributes:
        product_id: Primary key
        product_name: Name or classification of product
        category: Product category type
        product_weight: Net weight in kg
        fragility_index: Durability requirement (1-10)
        shipping_type: Mode of transportation
        created_at: Record creation timestamp
        updated_at: Record last update timestamp
    """
    
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(100), nullable=False)
    category = Column(String(100), index=True)
    product_weight = Column(Float, CheckConstraint('product_weight >= 0'))
    fragility_index = Column(
        Integer,
        CheckConstraint('fragility_index >= 1 AND fragility_index <= 10')
    )
    shipping_type = Column(
        String(50),
        CheckConstraint("shipping_type IN ('Air', 'Road', 'Sea', 'Rail')"),
        index=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    recommendations = relationship('RecommendationLog', back_populates='product', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Product(id={self.product_id}, name='{self.product_name}')>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'category': self.category,
            'product_weight': self.product_weight,
            'fragility_index': self.fragility_index,
            'shipping_type': self.shipping_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create model instance from dictionary"""
        return cls(
            product_name=data.get('product_name'),
            category=data.get('category'),
            product_weight=data.get('product_weight'),
            fragility_index=data.get('fragility_index'),
            shipping_type=data.get('shipping_type')
        )
