# app/api/user_schema.py

import re

from marshmallow import Schema, fields, validates, ValidationError


class LoginSchema(Schema):
    email = fields.Email(required=True,
                         error_messages={"required": "Email is required.", "invalid": "Invalid email format."})
    password = fields.Str(required=True, error_messages={"required": "Password is required."})

    @validates('password')
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError("Password must be at least 6 characters long.")


class RegisterSchema(Schema):
    username = fields.Str(required=True, error_messages={"required": "Username is required."})
    email = fields.Email(required=True,
                         error_messages={"required": "Email is required.", "invalid": "Invalid email format."})
    password = fields.Str(required=True, error_messages={"required": "Password is required."})
    confirm_password = fields.Str(required=True, error_messages={"required": "Confirm password is required."})

    @validates('password')
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError("Password must be at least 6 characters long.")
        if not re.search("[A-Za-z]", value) or not re.search("[0-9]", value):
            raise ValidationError("Password must contain both letters and numbers.")

    @validates('confirm_password')
    def validate_confirm_password(self, value, **kwargs):
        if 'password' in kwargs and value != kwargs['password']:
            raise ValidationError("Passwords do not match.")


class PasswordChangeSchema(Schema):
    """Schema for validating password change input"""

    current_password = fields.Str(required=True, error_messages={"required": "Current password is required."})
    new_password = fields.Str(required=True, error_messages={"required": "New password is required."})

    @validates('new_password')
    def validate_new_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise ValidationError("Password must contain at least one digit.")
        if not any(char.isupper() for char in value):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not any(char in '!@#$%^&*()_+' for char in value):
            raise ValidationError("Password must contain at least one special character.")
