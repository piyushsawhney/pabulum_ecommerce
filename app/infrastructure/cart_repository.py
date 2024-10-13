from app.domain.models.cart_items import CartItem
from app.infrastructure.db import db


class CartRepository:
    @staticmethod
    def add(cart_item):
        db.session.add(cart_item)
        db.session.commit()

    @staticmethod
    def get_cart_item(user_id, menu_item_id):
        return CartItem.query.filter_by(user_id=user_id, menu_item_id=menu_item_id).first()

    @staticmethod
    def get_user_cart(user_id):
        return CartItem.query.filter_by(user_id=user_id).all()

    @staticmethod
    def update(cart_item):
        db.session.commit()

    @staticmethod
    def delete(cart_item):
        db.session.delete(cart_item)
        db.session.commit()

    @staticmethod
    def empty_user_cart(user_id):
        CartItem.query.filter_by(user_id=user_id).delete()
        db.session.commit()