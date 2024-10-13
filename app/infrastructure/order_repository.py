from app.domain.models.orders import Order
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

    @staticmethod
    def update_order_status(razorpay_order_id, status):
        order = Order.query.filter_by(razorpay_order_id=razorpay_order_id).first()
        if order:
            order.status = status
            db.session.commit()
