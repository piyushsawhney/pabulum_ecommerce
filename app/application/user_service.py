# app/application/user_service.py


from app.application.auth_service import AuthService
from app.domain.models.user import User
from app.infrastructure.user_repository import UserRepository


class UserService:
    @staticmethod
    def register_user(username, email, password):
        if UserRepository.get_by_username(username):
            raise ValueError("Username already exists.")
        if UserRepository.get_by_email(email):
            raise ValueError("Email already exists.")

        password_hash = AuthService.hash_password(password)
        new_user = User(username=username, email=email, password_hash=password_hash)
        UserRepository.add(new_user)
        return new_user

    @staticmethod
    def login_user(email, password):
        user = UserRepository.get_by_email(email)
        if not user or not AuthService.check_password(password, user.password_hash):
            raise ValueError("Invalid email or password.")

        # Generate access and refresh tokens
        access_token = AuthService.generate_jwt(user.id, user.role)
        refresh_token = AuthService.generate_jwt(user.id, user.role, is_refresh=True)

        return {"access_token": access_token, "refresh_token": refresh_token}


