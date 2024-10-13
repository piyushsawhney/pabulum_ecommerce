# app/api/cart_routes.py

from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from app.application.cart_service import CartService

cart_bp = Blueprint('cart', __name__)

class AddToCartSchema(Schema):
    menu_item_id = fields.Int(required=True)
    quantity = fields.Int(required=False, default=1)

@cart_bp.route('/cart', methods=['POST'])
def add_to_cart():
    schema = AddToCartSchema()
    user_id = request.args.get('user_id')  # For demo purposes, we use query params for user ID
    try:
        cart_data = schema.load(request.json)
        cart_item = CartService.add_to_cart(
            user_id=user_id,
            menu_item_id=cart_data['menu_item_id'],
            quantity=cart_data.get('quantity', 1)
        )
        return jsonify({"message": "Item added to cart successfully!", "cart_item_id": cart_item.id}), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@cart_bp.route('/cart', methods=['GET'])
def view_cart():
    user_id = request.args.get('user_id')  # For demo purposes, we use query params for user ID
    cart_items = CartService.view_cart(user_id)
    return jsonify([{"id": item.id, "menu_item_id": item.menu_item_id, "quantity": item.quantity} for item in cart_items]), 200

@cart_bp.route('/cart/<int:menu_item_id>', methods=['DELETE'])
def remove_from_cart(menu_item_id):
    user_id = request.args.get('user_id')  # For demo purposes, we use query params for user ID
    try:
        CartService.remove_from_cart(user_id, menu_item_id)
        return jsonify({"message": "Item removed from cart successfully!"}), 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@cart_bp.route('/cart/empty', methods=['DELETE'])
def empty_cart():
    user_id = request.args.get('user_id')  # For demo purposes, we use query params for user ID
    CartService.empty_cart(user_id)
    return jsonify({"message": "Cart emptied successfully!"}), 204
