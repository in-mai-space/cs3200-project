from marshmallow import Schema, fields, validate

# Tony's code ========================================================
class UserSchema(Schema):
    """Schema for validating user data."""
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=50))
    type = fields.String(
        required=True,
        validate=validate.OneOf(['admin', 'user', 'data_analyst', 'organization_admin'])
    )
    registered_at = fields.DateTime(dump_only=True)  # automatically set by the database

class UserUpdateSchema(Schema):
    """Schema for validating user update data."""
    first_name = fields.String(validate=validate.Length(min=1, max=50))
    last_name = fields.String(validate=validate.Length(min=1, max=50))
    type = fields.String(validate=validate.OneOf(['admin', 'user', 'data_analyst', 'organization_admin']))