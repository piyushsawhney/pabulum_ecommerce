# app/api/order_routes.py

from flask import Blueprint, request, jsonify
from app.application.order_service import OrderService

order_bp = Blueprint('order', __name__)

@order_bp.route('/checkout', methods=['POST'])
def checkout():
    user_id = request.args.get('user_id')  # For demo purposes, we use query params for user ID
    try:
        order = OrderService.checkout(user_id)
        return jsonify({
            "message": "Order placed successfully!",
            "order_id": order.id,
            "total_amount": order.total_amount,
            "created_at": order.created_at
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
