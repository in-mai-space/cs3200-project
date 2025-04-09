from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime

class ProgramSchema(Schema):
    """Schema for validating program creation payload."""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    status = fields.Str(validate=validate.OneOf(['open', 'close']))
    start_date = fields.Date(allow_none=True)
    deadline = fields.DateTime(allow_none=True)
    end_date = fields.Date(allow_none=True)
    organization_id = fields.Str(required=True, validate=validate.Length(equal=36))
    category_id = fields.Str(required=True, validate=validate.Length(equal=36))

    def validate_dates(self, data, **kwargs):
        """Validate that dates are in correct order."""
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise ValidationError("Start date must be before end date")
        
        if data.get('deadline') and data.get('end_date'):
            if data['deadline'].date() > data['end_date']:
                raise ValidationError("Deadline must be before end date")

class ProgramUpdateSchema(Schema):
    """Schema for validating program update payload."""
    name = fields.Str(validate=validate.Length(min=1, max=100))
    description = fields.Str(validate=validate.Length(min=1))
    status = fields.Str(validate=validate.OneOf(['open', 'close']))
    start_date = fields.Date(allow_none=True)
    deadline = fields.DateTime(allow_none=True)
    end_date = fields.Date(allow_none=True)
    organization_id = fields.Str(validate=validate.Length(equal=36))
    category_id = fields.Str(validate=validate.Length(equal=36))

    def validate_dates(self, data, **kwargs):
        """Validate that dates are in correct order."""
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise ValidationError("Start date must be before end date")
        
        if data.get('deadline') and data.get('end_date'):
            if data['deadline'].date() > data['end_date']:
                raise ValidationError("Deadline must be before end date")
