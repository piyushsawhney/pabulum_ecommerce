# app/api/schemas/cart_schema.py

from marshmallow import Schema, fields, validate, ValidationError

class CartItemSchema(Schema):
    """Schema for validating Cart Item data."""
    menu_item_id = fields.Int(required=True, validate=validate.Range(min=1), error_messages={
        "required": "Menu item ID is required.",
        "null": "Menu item ID cannot be null.",
        "invalid": "Invalid value for Menu item ID."
    })
    quantity = fields.Int(required=True, validate=validate.Range(min=1), error_messages={
        "required": "Quantity is required.",
        "null": "Quantity cannot be null.",
        "invalid": "Quantity must be a positive integer."
    })

class RemoveCartItemSchema(Schema):
    """Schema for validating Cart Item removal data."""
    menu_item_id = fields.Int(required=True, validate=validate.Range(min=1), error_messages={
        "required": "Menu item ID is required.",
        "null": "Menu item ID cannot be null.",
        "invalid": "Invalid value for Menu item ID."
    })
