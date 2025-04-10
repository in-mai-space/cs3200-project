from marshmallow import Schema, fields, validate
class UserProfileSchema(Schema):
    """Schema for validating user profile data."""
    user_id = fields.String(required=True, validate=validate.Length(equal=36))
    ssn = fields.String(required=True, validate=validate.Length(max=11))
    
    # Verification status: must be one of the valid enum values with a default of 'unverified'
    verification_status = fields.String(
        missing='unverified',
        validate=validate.OneOf(['unverified', 'pending', 'verified'])
    )
