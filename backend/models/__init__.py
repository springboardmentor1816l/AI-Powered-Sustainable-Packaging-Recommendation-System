from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models for easy access
from .material import Material
from .product import Product
from .prediction import Prediction

__all__ = ['db', 'Material', 'Product', 'Prediction']
