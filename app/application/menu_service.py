# app/application/menu_service.py
from app.domain.models.menu_item import MenuItem
from app.infrastructure.menu_repository import MenuItemRepository


class MenuService:
    @staticmethod
    def add_menu_item(name, description, price):
        new_item = MenuItem(name=name, description=description, price=price)
        MenuItemRepository.add(new_item)
        return new_item

    @staticmethod
    def get_all_menu_items():
        return MenuItemRepository.get_all()

    @staticmethod
    def get_menu_item_by_id(item_id):
        return MenuItemRepository.get_by_id(item_id)

    @staticmethod
    def update_menu_item(item_id, name=None, description=None, price=None):
        item = MenuItemRepository.get_by_id(item_id)
        if item:
            if name:
                item.name = name
            if description:
                item.description = description
            if price is not None:
                item.price = price
            MenuItemRepository.update(item)
            return item
        else:
            raise ValueError("Menu item not found.")

    @staticmethod
    def delete_menu_item(item_id):
        item = MenuItemRepository.get_by_id(item_id)
        if item:
            MenuItemRepository.delete(item)
            return True
        else:
            raise ValueError("Menu item not found.")
