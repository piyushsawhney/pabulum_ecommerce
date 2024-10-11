# app/application/user_service.py


from werkzeug.security import generate_password_hash, check_password_hash

from app.domain.models.user import User
from app.infrastructure.user_repository import UserRepository


class UserService:
    @staticmethod
    def register_user(username, email, password):
        if UserRepository.get_by_username(username):
            raise ValueError("Username already exists.")
        if UserRepository.get_by_email(email):
            raise ValueError("Email already exists.")

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        UserRepository.add(new_user)
        return new_user

    @staticmethod
    def login_user(username_or_email, password):
        user = UserRepository.get_by_username(username_or_email) or UserRepository.get_by_email(username_or_email)
        if user and check_password_hash(user.password, password):
            return user
        else:
            raise ValueError("Invalid username/email or password.")
