from marshmallow import Schema, fields, validate

class CategorySchema(Schema):
    """Schema for validating category data."""
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))

class CategoryUpdateSchema(Schema):
    """Schema for validating category update data."""
    name = fields.String(validate=validate.Length(min=1, max=100))
