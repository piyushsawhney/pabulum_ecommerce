# app/main.py
import logging

from flask import Flask, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError

from app.api.routes.cart_routes import cart_bp
from app.api.routes.menu_routes import menu_bp
from app.api.routes.order_routes import order_bp
from app.api.secure_routes import secure_bp
from app.api.routes.user_routes import user_bp
from app.infrastructure.db import db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(secure_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()  # Create all database tables based on models

    # Error handling
    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        logging.error(f"Validation Error: {err.messages}")
        return jsonify({"error": err.messages}), 400

    @app.errorhandler(ValueError)
    def handle_value_error(err):
        logging.error(f"Value Error: {err}")
        return jsonify({"error": str(err)}), 400

    # @app.errorhandler(Exception)
    # def handle_generic_error(err):
    #     logging.error(f"Unexpected Error: {err}")
    #     return jsonify({"error": "An unexpected error occurred."}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
