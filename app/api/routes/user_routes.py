# app/api/user_routes.py

from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.api.auth_middleware import token_required
from app.api.schemas.user_schema import RegisterSchema, LoginSchema, PasswordChangeSchema
from app.application.auth_service import AuthService
from app.application.user_service import UserService
from app.domain.models.blacklist_tokens import BlacklistToken

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


@user_bp.route('/user/logout', methods=['POST'])
@token_required
def logout():
    """Log out the user and blacklist the token"""
    token = request.headers.get('Authorization').split(" ")[1]  # Get token from the header

    try:
        AuthService.blacklist_token(BlacklistToken(token=token))
        return jsonify({"message": "Successfully logged out."}), 200

    except Exception as e:
        return jsonify({"error": "Failed to log out."}), 500


@user_bp.route('/user/change_password', methods=['POST'])
@token_required
def change_password():
    """API endpoint to change the user's password"""
    user_id = request.user_id  # Extract user_id from the token
    token = request.headers.get('Authorization').split(" ")[1]  # Get token from the header

    # Load and validate the input data using the PasswordChangeSchema
    try:
        data = PasswordChangeSchema().load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    current_password = data.get('current_password')
    new_password = data.get('new_password')

    try:
        UserService.change_password(user_id=user_id, old_password=current_password, new_password=new_password,
                                    token=token)
        return jsonify({"message": "Password updated successfully. Please log in again."}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        return jsonify({"error": "Failed to log out."}), 500
