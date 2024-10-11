# app/application/user_service.py


from werkzeug.security import generate_password_hash

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
