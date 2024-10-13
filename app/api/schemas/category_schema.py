from marshmallow import Schema, fields, validates, ValidationError


class CategorySchema(Schema):
    """Schema for validating category input"""

    name = fields.Str(required=True, error_messages={"required": "Category name is required."})
    description = fields.Str(required=False)

    @validates('name')
    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError("Category name must be at least 3 characters long.")
        if len(value) > 100:
            raise ValidationError("Category name must be less than 100 characters.")
