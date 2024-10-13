# app/domain/models/blacklist_tokens.py

import datetime

from app.infrastructure.db import db


class BlacklistToken(db.Model):
    """Model for storing blacklisted tokens"""

    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now(datetime.UTC)

    def __repr__(self):
        return f'<BlacklistToken token={self.token}>'

    @staticmethod
    def check_blacklist(auth_token):
        """Check whether the token has been blacklisted"""
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True  # token is blacklisted
        return False

    def set_blacklisted_on(self, blacklisted_on):
        self.blacklisted_on = blacklisted_on
