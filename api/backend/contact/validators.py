from marshmallow import Schema, fields, validate

class PointOfContactSchema(Schema):
    """Schema for validating point of contact data."""
    id = fields.String(dump_only=True, validate=validate.Length(min=1, max=36))
    contact_type = fields.String(required=True, validate=validate.OneOf(['user', 'organization']))
    entity_id = fields.String(required=True, validate=validate.Length(min=1, max=36)) 
    description = fields.String(validate=validate.Length(max=100), allow_none=True)
    email = fields.Email(required=True, validate=validate.Length(max=100))
    phone_number = fields.String(validate=validate.Length(max=20), allow_none=True)
    created_at = fields.DateTime(dump_only=True)  # Automatically set by the DB
    updated_at = fields.DateTime(dump_only=True)  # Automatically updated by the DB

class PointOfContactUpdateSchema(Schema):
    """Schema for validating point of contact update data."""
    contact_type = fields.String(validate=validate.OneOf(['user', 'organization']))
    entity_id = fields.String(validate=validate.Length(min=1, max=36))
    description = fields.String(validate=validate.Length(max=100), allow_none=True)
    email = fields.Email(validate=validate.Length(max=100))
    phone_number = fields.String(validate=validate.Length(max=20), allow_none=True)