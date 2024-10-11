# app/main.py

from flask import Flask
from app.api.user_routes import user_bp
from app.infrastructure.db import db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(user_bp)

    with app.app_context():
        db.create_all()  # Create database tables

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
