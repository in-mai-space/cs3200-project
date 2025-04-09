from enum import Enum
from marshmallow import Schema, fields, validates, ValidationError, validate
from marshmallow_enum import EnumField

class ProgramStatus(str, Enum):
    OPEN = "open"
    CLOSE = "close"

class LocationType(str, Enum):
    VIRTUAL = "virtual"
    PHYSICAL = "physical"

class LocationBaseSchema(Schema):
    type = EnumField(LocationType, required=True)
    address_line1 = fields.Str(allow_none=True)
    address_line2 = fields.Str(allow_none=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    zip_code = fields.Str(required=True)
    country = fields.Str(missing="United States")
    is_primary = fields.Bool(missing=True)

    @validates("zip_code")
    def validate_zip_code(self, value):
        if not value.isdigit() or len(value) not in [5, 9]:
            raise ValidationError("Zip code must be 5 or 9 digits")

class ProgramBaseSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    status = EnumField(ProgramStatus, missing=ProgramStatus.OPEN)
    start_date = fields.Date(required=True)
    deadline = fields.DateTime(required=True)
    end_date = fields.Date(allow_none=True)
    organization_id = fields.Str(required=True, validate=validate.Length(equal=36))
    category_id = fields.Str(required=True, validate=validate.Length(equal=36))
    locations = fields.List(fields.Nested(LocationBaseSchema), required=True, validate=validate.Length(min=1))

    @validates("end_date")
    def validate_end_date(self, value, **kwargs):
        start_date = self.context.get("start_date")
        if value and start_date and value < start_date:
            raise ValidationError("end_date must be after start_date")

    @validates("deadline")
    def validate_deadline(self, value, **kwargs):
        start_date = self.context.get("start_date")
        if start_date and value.date() < start_date:
            raise ValidationError("deadline must be after start_date")

class ProgramCreateSchema(ProgramBaseSchema):
    pass

class ProgramUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=100))
    description = fields.Str(validate=validate.Length(min=1))
    status = EnumField(ProgramStatus, allow_none=True)
    start_date = fields.Date(allow_none=True)
    deadline = fields.DateTime(allow_none=True)
    end_date = fields.Date(allow_none=True)
    organization_id = fields.Str(validate=validate.Length(equal=36), allow_none=True)
    category_id = fields.Str(validate=validate.Length(equal=36), allow_none=True)
    locations = fields.List(fields.Nested(LocationBaseSchema), allow_none=True)

    @validates("end_date")
    def validate_end_date(self, value, **kwargs):
        start_date = self.context.get("start_date")
        if value and start_date and value < start_date:
            raise ValidationError("end_date must be after start_date")

    @validates("deadline")
    def validate_deadline(self, value, **kwargs):
        start_date = self.context.get("start_date")
        if start_date and value.date() < start_date:
            raise ValidationError("deadline must be after start_date")

class SearchQueryParamSchema(Schema):
    search_query = fields.Str(allow_none=True)
    categories = fields.List(fields.Str(), allow_none=True)
    location = fields.Dict(keys=fields.Str(), values=fields.Str(), allow_none=True)
    is_qualified = fields.Bool(allow_none=True)
    sort_by = fields.Str(
        validate=validate.Regexp("^(name|start_date|deadline)$"),
        allow_none=True
    )
    sort_order = fields.Str(
        validate=validate.Regexp("^(asc|desc)$"),
        allow_none=True
    )

    @validates("location")
    def validate_location(self, value):
        allowed_fields = {"city", "state", "zip_code", "country"}
        if not all(k in allowed_fields for k in value):
            raise ValidationError("Invalid location field")

    @validates("categories")
    def validate_categories(self, value):
        if not all(isinstance(cat, str) for cat in value):
            raise ValidationError("Categories must be strings")

    @validates("is_qualified")
    def validate_is_qualified(self, value):
        if not isinstance(value, bool):
            raise ValidationError("is_qualified must be a boolean")
