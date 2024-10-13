# app/application/auth_service.py

import datetime
import os
import pytz
import bcrypt
import jwt
from dotenv import load_dotenv
from flask import jsonify

from app.domain.models.blacklist import BlacklistToken
from app.infrastructure.auth_repository import AuthRepository
from app.infrastructure.user_repository import UserRepository

# Load environment variables
load_dotenv()


class AuthService:

    @staticmethod
    def hash_password(password):
        """Hash the password securely using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def check_password(password, hashed):
        """Check if the provided password matches the hashed password."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @staticmethod
    def generate_jwt(user_id, role, is_refresh=False):
        """Generate JWT token (access or refresh) with expiration."""
        secret_key = os.getenv("JWT_SECRET")
        expiration = datetime.datetime.now(datetime.UTC) + (
            datetime.timedelta(minutes=15) if not is_refresh else datetime.timedelta(days=30)
        )
        payload = {
            'user_id': user_id,
            'role': role,  # Include role in token
            'exp': expiration
        }

        # Encode JWT
        token = jwt.encode(payload, secret_key, algorithm='HS256')

        # Ensure token is a string, not bytes (depending on PyJWT version)
        return token if isinstance(token, str) else token.decode('utf-8')

    @staticmethod
    def decode_jwt(token):
        """Decode the JWT token and return the payload."""
        secret_key = os.getenv("JWT_SECRET")
        try:
            # Decode JWT, returns the decoded payload
            decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
            user = UserRepository.get_by_id(decoded['user_id'])
            issued_at = datetime.datetime.fromtimestamp(decoded.get('exp'), datetime.UTC)
            # Check if token was issued before the last password change
            if user.last_password_change and issued_at < pytz.utc.localize(user.last_password_change):
                return jsonify({'message': 'Token invalid due to password change. Please log in again.'}), 401

            # Check if the token is blacklisted
            if BlacklistToken.check_blacklist(token):
                return jsonify({'message': 'Token has been blacklisted. Please log in again.'}), 401

            return decoded
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired.")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token.")

    @staticmethod
    def blacklist_token(token):
        AuthRepository.add(token)
