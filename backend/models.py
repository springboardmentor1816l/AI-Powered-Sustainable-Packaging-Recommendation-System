from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from .extensions import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    product_weight_kg = Column(Float)
    fragility_index = Column(Float)
    shipping_type = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    material_type = Column(String, index=True)
    recyclability_pct = Column(Float)
    load_handling_score = Column(Float)
    moisture_resistance_score = Column(Float)
    thermal_resistance_score = Column(Float)
    sustainability_score = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id"))
    material_id = Column(Integer, ForeignKey("materials.id"))

    predicted_cost = Column(Float)
    predicted_co2 = Column(Float)
    final_score = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
