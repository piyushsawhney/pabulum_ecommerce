# app/domain/user.py

from app.infrastructure.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Customer')  # Add role

    # Define roles
    ROLE_ADMIN = 'Admin'
    ROLE_CUSTOMER = 'Customer'
    ROLE_SELLER = 'Seller'

    def __init__(self, username, email, password_hash, role=ROLE_CUSTOMER):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
    
    def __repr__(self):
        return f'<User {self.username}>'
