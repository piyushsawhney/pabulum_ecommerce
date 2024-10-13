# app/api/schemas/menu_schema.py

from marshmallow import Schema, fields, validate, ValidationError

class MenuItemSchema(Schema):
    """Schema for validating Menu Item data."""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100), error_messages={
        "required": "Name is required",
        "null": "Name cannot be null",
        "invalid": "Invalid data for Name"
    })
    description = fields.Str(required=True, validate=validate.Length(min=5, max=300), error_messages={
        "required": "Description is required",
        "null": "Description cannot be null",
        "invalid": "Invalid data for Description"
    })
    price = fields.Float(required=True, validate=validate.Range(min=0.01), error_messages={
        "required": "Price is required",
        "null": "Price cannot be null",
        "invalid": "Price must be a positive number"
    })
    available = fields.Bool(required=True, error_messages={
        "required": "Availability status is required",
        "null": "Available cannot be null",
        "invalid": "Invalid value for Available"
    })
