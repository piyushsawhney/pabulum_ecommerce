# app/domain/menu_items.py

from app.infrastructure.db import db


class Category(db.Model):
    """Category model for menu items"""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)
    menu_items = db.relationship('MenuItem', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def __repr__(self):
        return f'<MenuItem {self.name}>'
