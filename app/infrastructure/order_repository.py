from app.infrastructure.db import db


class OrderRepository:
    @staticmethod
    def create_order(order):
        db.session.add(order)
        db.session.commit()

    @staticmethod
    def add_order_item(order_item):
        db.session.add(order_item)
        db.session.commit()