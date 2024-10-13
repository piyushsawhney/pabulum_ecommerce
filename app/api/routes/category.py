from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app import db
from app.api.auth_middleware import token_required, role_required
from app.api.schemas.category_schema import CategorySchema
from app.domain.models.categories import Category


category_bp = Blueprint('category_bp', __name__)


# POST /categories (Admin Only)
@category_bp.route('/admin/categories', methods=['POST'])
@token_required
@role_required('Admin')
def create_category():
    """Create a new category (Admin only)"""
    try:
        data = CategorySchema().load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    name = data['name']
    description = data.get('description', '')

    # Check if category already exists
    if Category.query.filter_by(name=name).first():
        return jsonify({"error": "Category already exists."}), 400

    category = Category(name=name, description=description)
    db.session.add(category)
    db.session.commit()

    return jsonify({"message": "Category created successfully."}), 201


# GET /categories (All Users)
@category_bp.route('/menu/categories', methods=['GET'])
@token_required
def get_categories():
    """Fetch all categories (All users)"""
    categories = Category.query.all()
    category_list = [{"id": c.id, "name": c.name, "description": c.description} for c in categories]
    return jsonify(category_list), 200


# PUT /categories/<int:id> (Admin Only)
@category_bp.route('/admin/categories/<int:id>', methods=['PUT'])
@token_required
@role_required('Admin')
def update_category(id):
    """Update an existing category (Admin only)"""
    try:
        data = CategorySchema().load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    category = Category.query.get_or_404(id)
    category.name = data['name']
    category.description = data.get('description', category.description)

    db.session.commit()

    return jsonify({"message": "Category updated successfully."}), 200


# DELETE /categories/<int:id> (Admin Only)
@category_bp.route('/admin/categories/<int:id>', methods=['DELETE'])
@token_required
@role_required('Admin')
def delete_category(id):
    """Delete a category (Admin only)"""
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Category deleted successfully."}), 200
