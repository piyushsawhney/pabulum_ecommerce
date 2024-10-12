# app/api/menu_routes.py

from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from app.application.menu_service import MenuService

menu_bp = Blueprint('menu', __name__)

class MenuItemSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=False)
    price = fields.Float(required=True)

class UpdateMenuItemSchema(Schema):
    name = fields.Str(required=False)
    description = fields.Str(required=False)
    price = fields.Float(required=False)

@menu_bp.route('/menu', methods=['POST'])
def add_menu_item():
    schema = MenuItemSchema()
    try:
        menu_data = schema.load(request.json)
        menu_item = MenuService.add_menu_item(
            name=menu_data['name'],
            description=menu_data.get('description'),
            price=menu_data['price']
        )
        return jsonify({"message": "Menu item added successfully!", "item_id": menu_item.id}), 201
    except ValidationError as err:
        return jsonify(err.messages), 400

@menu_bp.route('/menu', methods=['GET'])
def get_all_menu_items():
    menu_items = MenuService.get_all_menu_items()
    return jsonify([{"id": item.id, "name": item.name, "description": item.description, "price": item.price} for item in menu_items]), 200

@menu_bp.route('/menu/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    try:
        menu_item = MenuService.get_menu_item_by_id(item_id)
        return jsonify({"id": menu_item.id, "name": menu_item.name, "description": menu_item.description, "price": menu_item.price}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@menu_bp.route('/menu/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    schema = UpdateMenuItemSchema()
    try:
        update_data = schema.load(request.json)
        menu_item = MenuService.update_menu_item(item_id, **update_data)
        return jsonify({"message": "Menu item updated successfully!", "item": {"id": menu_item.id, "name": menu_item.name   , "description": menu_item.description, "price": menu_item.price}}), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@menu_bp.route('/menu/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    try:
        MenuService.delete_menu_item(item_id)
        return jsonify({"message": "Menu item deleted successfully!"}), 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
