import sys
sys.path.insert(0, 'backend')

from app import app
from models import db

with app.app_context():
    db.create_all()
    print("✓ Database tables created successfully!")
