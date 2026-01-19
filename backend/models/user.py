"""
User Model
==========

SQLAlchemy model for user authentication.

Author: EcoPackAI Team
Date: 2026-01-03
"""

from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db

class User(db.Model):
    """
    User model - stores user authentication and authorization data
    
    Attributes:
        user_id: Primary key
        username: Unique username for login
        email: User email address
        password_hash: Hashed password
        role: User access level (admin, user, viewer)
        created_at: Account creation timestamp
        last_login: Last successful login timestamp
    """
    
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        String(50),
        CheckConstraint("role IN ('admin', 'user', 'viewer')"),
        default='user',
        nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<User(id={self.user_id}, username='{self.username}', role='{self.role}')>"
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = func.now()
    
    def to_dict(self, include_sensitive=False):
        """
        Convert model to dictionary
        
        Args:
            include_sensitive: Include password hash (default: False)
        """
        data = {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        
        if include_sensitive:
            data['password_hash'] = self.password_hash
        
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create model instance from dictionary"""
        user = cls(
            username=data.get('username'),
            email=data.get('email'),
            role=data.get('role', 'user')
        )
        
        if 'password' in data:
            user.set_password(data['password'])
        
        return user
    
    def has_permission(self, required_role):
        """
        Check if user has required permission level
        
        Args:
            required_role: Required role ('admin', 'user', 'viewer')
            
        Returns:
            bool: True if user has permission
        """
        role_hierarchy = {'viewer': 0, 'user': 1, 'admin': 2}
        return role_hierarchy.get(self.role, 0) >= role_hierarchy.get(required_role, 0)
