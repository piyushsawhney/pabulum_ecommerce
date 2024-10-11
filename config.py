# app/config.py

import os

class Config:
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///ecommerce.db")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
