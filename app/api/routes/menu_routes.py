# app/api/menu_routes.py

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.api.schemas.menu_schema import MenuItemSchema
from app.application.menu_service import MenuService

menu_bp = Blueprint('menu', __name__)


@menu_bp.route('/menu', methods=['POST'])
def add_menu_item():
    try:
        # Validate incoming JSON payload using the schema
        data = MenuItemSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    is_available = data.get('is_available')

    try:
        # Call the service to handle business logic for creating menu item
        menu_item = MenuService.add_menu_item(name, description, price, is_available)
        return jsonify({
            "message": "Menu item created successfully!",
            "menu_item": {
                "id": menu_item.id,
                "name": menu_item.name,
                "description": menu_item.description,
                "price": menu_item.price,
                "is_available": menu_item.is_available
            }
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500


@menu_bp.route('/menu', methods=['GET'])
def get_all_menu_items():
    menu_items = MenuService.get_all_menu_items()
    return jsonify(
        [{"id": menu_item.id, "name": menu_item.name, "description": menu_item.description, "price": menu_item.price,
          "is_available": menu_item.is_available} for menu_item in
         menu_items]), 200


@menu_bp.route('/menu/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    try:
        menu_item = MenuService.get_menu_item_by_id(item_id)
        return jsonify(
            {"id": menu_item.id, "name": menu_item.name, "description": menu_item.description, "price": menu_item.price,
             "is_available": menu_item.is_available}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@menu_bp.route('/menu/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    """Update an existing menu item with input validation."""
    try:
        # Validate the incoming JSON payload using the schema
        data = MenuItemSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    is_available = data.get('is_available')

    try:
        # Call the service to handle the update logic
        updated_item = MenuService.update_menu_item(item_id, name, description, price, is_available)
        return jsonify({
            "message": "Menu item updated successfully!",
            "menu_item": {
                "id": updated_item.id,
                "name": updated_item.name,
                "description": updated_item.description,
                "price": updated_item.price,
                "is_available": updated_item.is_available
            }
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred."}), 500


@menu_bp.route('/menu/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    try:
        MenuService.delete_menu_item(item_id)
        return jsonify({"message": "Menu item deleted successfully!"}), 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
