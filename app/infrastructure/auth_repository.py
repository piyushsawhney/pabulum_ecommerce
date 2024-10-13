# app/infrastructure/repositories.py
from app.infrastructure.db import db


class AuthRepository:
    @staticmethod
    def add(blacklist_token):
        db.session.add(blacklist_token)
        db.session.commit()
