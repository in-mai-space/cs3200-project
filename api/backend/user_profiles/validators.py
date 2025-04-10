from marshmallow import Schema, fields, validate
class UserProfileSchema(Schema):
    """Schema for validating user profile data."""
    user_id = fields.String(required=True, validate=validate.Length(equal=36))
    ssn = fields.String(required=True, validate=validate.Length(max=11))
    
    date_of_birth = fields.Date(required=False)
    gender = fields.String(required=False)
    income = fields.Float(required=False)
    education_level = fields.String(required=False)
    employment_status = fields.String(required=False)
    veteran_status = fields.Boolean(required=False)
    disability_status = fields.Boolean(required=False)
    verification_date = fields.DateTime(required=False)

    # Verification status: must be one of the valid enum values with a default of 'unverified'
    verification_status = fields.String(
        missing='unverified',
        validate=validate.OneOf(['unverified', 'pending', 'verified'])
    )
