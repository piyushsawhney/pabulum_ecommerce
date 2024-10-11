# app/application/order_service.py
from app.domain.models.order import Order, OrderItem
from app.infrastructure.cart_repository import CartRepository
from app.infrastructure.order_repository import OrderRepository


class OrderService:
    @staticmethod
    def checkout(user_id):
        cart_items = CartRepository.get_user_cart(user_id)
        if not cart_items:
            raise ValueError("Cart is empty. Cannot proceed with checkout.")

        total_amount = sum(item.menu_item.price * item.quantity for item in cart_items)

        # Create order
        order = Order(user_id=user_id, total_amount=total_amount)
        OrderRepository.create_order(order)

        # Create order items and save them
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=cart_item.menu_item_id,
                quantity=cart_item.quantity,
                price=cart_item.menu_item.price
            )
            OrderRepository.add_order_item(order_item)

        # Clear the user's cart after checkout
        CartRepository.empty_user_cart(user_id)

        return order
