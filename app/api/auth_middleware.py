# app/api/auth_middleware.py

from functools import wraps

from flask import request, jsonify

from app.application.auth_service import AuthService
from app.infrastructure.user_repository import UserRepository


def token_required(f):
    """A decorator that ensures the user is authenticated via JWT token."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            decoded = AuthService.decode_jwt(token)
        except ValueError as e:
            return jsonify({"error": str(e)}), 401
        request.user_id = decoded['user_id']
        return f(*args, **kwargs)

    return decorated


def role_required(required_role):
    """A decorator that checks if the authenticated user has the required role."""

    def decorator(f):
        @wraps(f)
        def decorated_function(user_id, *args, **kwargs):
            # Fetch the user from the database
            user = UserRepository.get_by_id(user_id)

            if not user:
                return jsonify({"error": "User not found."}), 404

            # Check if the user has the required role
            if user.role != required_role:
                return jsonify({"error": "Access denied. Role mismatch."}), 403

            return f(user_id=user_id, *args, **kwargs)

        return decorated_function

    return decorator
