from app.domain.models.menu_items import MenuItem
from app.infrastructure.db import db


class MenuItemRepository:
    @staticmethod
    def add(menu_item):
        db.session.add(menu_item)
        db.session.commit()

    @staticmethod
    def get_all():
        return MenuItem.query.all()

    @staticmethod
    def get_by_id(item_id):
        return MenuItem.query.get(item_id)

    @staticmethod
    def update(menu_item):
        db.session.commit()

    @staticmethod
    def delete(menu_item):
        db.session.delete(menu_item)
        db.session.commit()