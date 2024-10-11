# app/api/user_routes.py

from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from app.application.user_service import UserService

user_bp = Blueprint('user', __name__)

class UserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class LoginSchema(Schema):
    username_or_email = fields.Str(required=True)
    password = fields.Str(required=True)

@user_bp.route('/register', methods=['POST'])
def register():
    schema = UserSchema()
    try:
        user_data = schema.load(request.json)
        user = UserService.register_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        return jsonify({"message": "User registered successfully!", "user_id": user.id}), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route('/login', methods=['POST'])
def login():
    schema = LoginSchema()
    try:
        login_data = schema.load(request.json)
        user = UserService.login_user(
            username_or_email=login_data['username_or_email'],
            password=login_data['password']
        )
        return jsonify({"message": "Login successful!", "user_id": user.id}), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400