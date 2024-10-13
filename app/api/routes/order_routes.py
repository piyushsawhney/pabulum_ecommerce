# app/api/order_routes.py

from flask import Blueprint, request, jsonify
from app.application.order_service import OrderService
from app.infrastructure.order_repository import OrderRepository

order_bp = Blueprint('order', __name__)

@order_bp.route('/checkout', methods=['POST'])
def checkout():
    user_id = request.user_id
    try:
        payment_data = OrderService.checkout(user_id)
        return jsonify({
            "message": "Order placed successfully!",
            "order_id": payment_data['order'].id,
            # "razorpay_order_id": payment_data['razorpay_order_id'],
            "total_amount": payment_data['total_amount'],
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@order_bp.route('/payment/success', methods=['POST'])
def payment_success():
    payload = request.json
    razorpay_order_id = payload.get('razorpay_order_id')
    razorpay_payment_id = payload.get('razorpay_payment_id')
    razorpay_signature = payload.get('razorpay_signature')

    # Verify Razorpay signature to ensure the request is legitimate
    is_valid = OrderService.verify_payment_signature(
        razorpay_order_id, razorpay_payment_id, razorpay_signature
    )

    if is_valid:
        # Update the order status to "paid"
        OrderRepository.update_order_status(razorpay_order_id, "paid")
        return jsonify({"message": "Payment successful!"}), 200
    else:
        return jsonify({"error": "Payment verification failed!"}), 400
