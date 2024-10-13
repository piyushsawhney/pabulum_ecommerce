# app/application/order_service.py
import hashlib
import hmac

import razorpay

from app.domain.models.menu_items import MenuItem
from app.domain.models.orders import Order, OrderItem
from app.infrastructure.cart_repository import CartRepository
from app.infrastructure.order_repository import OrderRepository
from config import Config


class OrderService:
    # razorpay_client = razorpay.Client(auth=(Config.RAZORPAY_KEY_ID, Config.RAZORPAY_KEY_SECRET))

    @staticmethod
    def checkout(user_id):
        cart_items = CartRepository.get_user_cart(user_id)
        if not cart_items:
            raise ValueError("Cart is empty. Cannot proceed with checkout.")
        total_amount = 0
        # Iterate through the cart items to calculate the total amount
        order_items = []
        for cart_item in cart_items:
            # Fetch the MenuItem associated with the menu_item_id
            menu_item = MenuItem.query.get(cart_item.menu_item_id)
            if not menu_item:
                raise ValueError(f"MenuItem with ID {cart_item.menu_item_id} not found.")

            # Calculate the price for the cart item and add it to the total
            item_total = menu_item.price * cart_item.quantity
            total_amount += item_total

            # Create an OrderItem
            order_item = OrderItem(
                menu_item_id=menu_item.id,
                quantity=cart_item.quantity,
                price=menu_item.price
            )
            order_items.append(order_item)

        # Convert the amount to paise (since Razorpay deals with the smallest currency unit)
        # amount_in_paise = int(total_amount * 100)

        # # Create Razorpay order
        # payment_order = OrderService.razorpay_client.order.create({
        #     'amount': amount_in_paise,
        #     'currency': 'INR',
        #     'payment_capture': 1  # Auto capture payment
        # })

        # Create a local order in the database
        order = Order(user_id=user_id, total_amount=total_amount)
        OrderRepository.create_order(order)

        # Save all the order items to the order
        for order_item in order_items:
            order_item.order_id = order.id
            OrderRepository.add_order_item(order_item)

        # Clear the user's cart after checkout
        CartRepository.empty_user_cart(user_id)

        # Return the order details along with the Razorpay order ID
        return {
            'order': order,
            # 'razorpay_order_id': payment_order['id'],
            'total_amount': total_amount
        }

    @staticmethod
    def verify_payment_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
        secret = Config.RAZORPAY_KEY_SECRET
        payload = f"{razorpay_order_id}|{razorpay_payment_id}"
        generated_signature = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

        return hmac.compare_digest(generated_signature, razorpay_signature)
