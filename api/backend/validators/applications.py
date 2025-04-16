from marshmallow import Schema, fields, validate

class ApplicationSchema(Schema):
    """Schema for validating new application payloads."""
    user_id = fields.String(
        required=True,
        validate=validate.Length(equal=36),
        error_messages={"required": "user_id is required"}
    )
    status = fields.String(
        missing='draft',
        validate=validate.OneOf([
            'draft', 'submitted', 'under_review',
            'additional_info_needed', 'approved',
            'rejected', 'waitlisted', 'withdrawn'
        ])
    )
    qualification_status = fields.String(
        missing='pending',
        validate=validate.OneOf([
            'pending', 'verified', 'incomplete', 'rejected'
        ])
    )
    decision_date = fields.DateTime(required=False)
    decision_notes = fields.String(required=False)