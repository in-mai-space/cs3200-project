from marshmallow import Schema, fields

class OrganizationSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    website_url = fields.String(required=True)
    is_verified = fields.Boolean(required=True)
    verified_at = fields.DateTime(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class OrganizationContactSchema(Schema):
    description = fields.String(required=True)
    email = fields.String(required=True)
    phone_number = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

