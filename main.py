# app/main.py

from flask import Flask
from flask_migrate import Migrate

from app.api.user_routes import user_bp
from app.api.menu_routes import menu_bp
from app.api.cart_routes import cart_bp
from app.api.order_routes import order_bp
from app.infrastructure.db import db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()  # Create all database tables based on models

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
