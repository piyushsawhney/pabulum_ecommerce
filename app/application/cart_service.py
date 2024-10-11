# app/application/cart_service.py
from app.domain.models.cart_item import CartItem
from app.infrastructure.cart_repository import CartRepository


class CartService:
    @staticmethod
    def add_to_cart(user_id, menu_item_id, quantity=1):
        cart_item = CartRepository.get_cart_item(user_id, menu_item_id)
        if cart_item:
            cart_item.quantity += quantity
            CartRepository.update(cart_item)
            return cart_item
        else:
            new_item = CartItem(user_id=user_id, menu_item_id=menu_item_id, quantity=quantity)
            CartRepository.add(new_item)
            return new_item

    @staticmethod
    def view_cart(user_id):
        return CartRepository.get_user_cart(user_id)

    @staticmethod
    def remove_from_cart(user_id, menu_item_id):
        cart_item = CartRepository.get_cart_item(user_id, menu_item_id)
        if cart_item:
            CartRepository.delete(cart_item)
            return True
        else:
            raise ValueError("Cart item not found.")

    @staticmethod
    def empty_cart(user_id):
        CartRepository.empty_user_cart(user_id)
