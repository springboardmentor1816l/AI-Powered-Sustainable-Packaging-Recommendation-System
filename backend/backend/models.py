from sqlalchemy import Column, Integer, String, Float, TIMESTAMP
from .database import Base

class Material(Base):
    __tablename__ = "materials"

    material_id = Column(Integer, primary_key=True, index=True)
    material_type = Column(String)
    strength_mpa = Column(Float)
    weight_capacity = Column(Float)
    biodegradability_percent = Column(Float)
    co2_emission_score = Column(Float)
    recyclability_percent = Column(Float)
    cost_per_kg = Column(Float)
    industry_use_case = Column(String)

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    category = Column(String)
    product_weight = Column(Float)
    fragility_index = Column(Integer)
    shipping_type = Column(String)
