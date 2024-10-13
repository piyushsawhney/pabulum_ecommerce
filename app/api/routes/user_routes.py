# app/api/user_routes.py

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.api.schemas.user_schema import RegisterSchema, LoginSchema
from app.application.auth_service import AuthService
from app.application.user_service import UserService

user_bp = Blueprint('user', __name__)


@user_bp.route('/user/register', methods=['POST'])
def register():
    try:
        data = RegisterSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    try:
        user = UserService.register_user(
            username=username,
            email=email,
            password=password
        )
        return jsonify({
            "message": "User registered successfully!",
            "user": {
                "id": user.id,
                "name": user.username,
                "email": user.email,
                "role": user.role
            }
        }), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route('/user/login', methods=['POST'])
def login():
    schema = LoginSchema()
    try:
        login_data = schema.load(request.json)
        token = UserService.login_user(
            email=login_data['email'],
            password=login_data['password']
        )
        return jsonify({"message": "Login successful!", "tokens": token}), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@user_bp.route('/user/refresh', methods=['POST'])
def refresh_token():
    refresh_token = request.json.get('refresh_token')
    try:
        decoded_payload = AuthService.decode_jwt(refresh_token)
        new_access_token = AuthService.generate_jwt(decoded_payload["user_id"], decoded_payload["role"])
        return jsonify({
            "access_token": new_access_token
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
