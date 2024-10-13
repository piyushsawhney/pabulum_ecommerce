# app/api/cart_routes.py

from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError

from app.api.auth_middleware import token_required
from app.api.schemas.cart_schema import CartItemSchema, RemoveCartItemSchema
from app.application.cart_service import CartService

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/cart', methods=['POST'])
@token_required
def add_to_cart():
    """Add a menu item to the user's cart."""
    try:
        # Validate the incoming JSON payload using the schema
        data = CartItemSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    menu_item_id = data.get('menu_item_id')
    quantity = data.get('quantity')

    try:
        # Extract user_id from the request context (set by token_required decorator)
        user_id = request.user_id

        # Call the service to handle business logic for adding an item to the cart
        cart_item = CartService.add_to_cart(user_id, menu_item_id, quantity)
        return jsonify({
            "message": "Item added to cart successfully!",
            "cart_item": {
                "menu_item_id": cart_item.menu_item_id,
                "quantity": cart_item.quantity
            }
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500

@cart_bp.route('/cart', methods=['GET'])
@token_required
def view_cart():
    user_id = request.user_id  # For demo purposes, we use query params for user ID
    cart_items = CartService.view_cart(user_id)
    return jsonify([{"id": item.id, "menu_item_id": item.menu_item_id, "quantity": item.quantity} for item in cart_items]), 200

@cart_bp.route('/cart/remove', methods=['DELETE'])
@token_required
def remove_from_cart():
    """Remove a menu item from the user's cart."""
    try:
        # Validate the incoming JSON payload using the schema
        data = RemoveCartItemSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    menu_item_id = data.get('menu_item_id')

    try:
        # Extract user_id from the request context (set by token_required decorator)
        user_id = request.user_id

        # Call the service to handle business logic for removing an item from the cart
        CartService.remove_from_cart(user_id, menu_item_id)
        return jsonify({
            "message": "Item removed from cart successfully!",
            "menu_item_id": menu_item_id
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500

@cart_bp.route('/cart/empty', methods=['DELETE'])
@token_required
def empty_cart():
    user_id = request.user_id
    CartService.empty_cart(user_id)
    return jsonify({"message": "Cart emptied successfully!"}), 204
