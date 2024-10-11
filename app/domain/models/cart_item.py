# app/domain/cart_item.py

from app.infrastructure.db import db

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<CartItem user_id={self.user_id}, menu_item_id={self.menu_item_id}, quantity={self.quantity}>'
