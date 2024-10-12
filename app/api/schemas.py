# app/api/schemas.py

from marshmallow import Schema, fields, validates, ValidationError
import re

class LoginSchema(Schema):
    email = fields.Email(required=True, error_messages={"required": "Email is required.", "invalid": "Invalid email format."})
    password = fields.Str(required=True, error_messages={"required": "Password is required."})

    @validates('password')
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError("Password must be at least 6 characters long.")

class RegisterSchema(Schema):
    username = fields.Str(required=True, error_messages={"required": "Username is required."})
    email = fields.Email(required=True, error_messages={"required": "Email is required.", "invalid": "Invalid email format."})
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
