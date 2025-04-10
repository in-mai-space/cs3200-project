from enum import Enum
from marshmallow import Schema, fields, validates, ValidationError, validate, validates_schema
from marshmallow_enum import EnumField

class ProgramStatus(str, Enum):
    OPEN = "open"
    CLOSE = "close"

class LocationType(str, Enum):
    VIRTUAL = "virtual"
    PHYSICAL = "physical"

class QualificationType(str, Enum):
    INCOME = "income"
    AGE = "age"
    FAMILY_SIZE = "family_size"
    LOCATION = "location"
    EDUCATION = "education"
    DISABILITY = "disability"
    VETERAN_STATUS = "veteran_status"
    CITIZENSHIP = "citizenship"
    OTHER = "other"

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

class QualificationSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    qualification_type = EnumField(QualificationType, required=True)
    min_value = fields.Decimal(allow_none=True)
    max_value = fields.Decimal(allow_none=True)
    text_value = fields.Str(allow_none=True)
    boolean_value = fields.Bool(allow_none=True)

    @validates("min_value")
    def validate_min_value(self, value):
        if value is not None and value < 0:
            raise ValidationError("min_value cannot be negative")

    @validates("max_value")
    def validate_max_value(self, value):
        if value is not None and value < 0:
            raise ValidationError("max_value cannot be negative")

    @validates_schema
    def validate_qualification_values(self, data):
        qual_type = data.get('qualification_type')
        
        if qual_type == QualificationType.INCOME:
            if data.get('min_value') is None and data.get('max_value') is None:
                raise ValidationError("Income qualification requires at least min_value or max_value")
        elif qual_type == QualificationType.AGE:
            if data.get('min_value') is None and data.get('max_value') is None:
                raise ValidationError("Age qualification requires at least min_value or max_value")
        elif qual_type == QualificationType.FAMILY_SIZE:
            if data.get('min_value') is None and data.get('max_value') is None:
                raise ValidationError("Family size qualification requires at least min_value or max_value")
        elif qual_type == QualificationType.LOCATION:
            if data.get('text_value') is None:
                raise ValidationError("Location qualification requires text_value")
        elif qual_type == QualificationType.EDUCATION:
            if data.get('text_value') is None and data.get('min_value') is None:
                raise ValidationError("Education qualification requires text_value or min_value")
        elif qual_type in [QualificationType.DISABILITY, QualificationType.VETERAN_STATUS]:
            if data.get('boolean_value') is None:
                raise ValidationError(f"{qual_type.value} qualification requires boolean_value")
        elif qual_type == QualificationType.OTHER:
            if data.get('text_value') is None and data.get('boolean_value') is None:
                raise ValidationError("Other qualification requires text_value or boolean_value")

class ProgramBaseSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    status = EnumField(ProgramStatus, missing=ProgramStatus.OPEN)
    start_date = fields.Date(required=True)
    deadline = fields.DateTime(required=True)
    end_date = fields.Date(allow_none=True)

    @validates("end_date")
    def validate_end_date(self, value):
        start_date = self.context.get("start_date")
        if value and start_date and value < start_date:
            raise ValidationError("end_date must be after start_date")

    @validates("deadline")
    def validate_deadline(self, value):
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

    @validates("end_date")
    def validate_end_date(self, value):
        start_date = self.context.get("start_date")
        if value and start_date and value < start_date:
            raise ValidationError("end_date must be after start_date")

    @validates("deadline")
    def validate_deadline(self, value):
        start_date = self.context.get("start_date")
        if start_date and value.date() < start_date:
            raise ValidationError("deadline must be after start_date")
        
class ProgramLocationSchema(Schema):
    locations = fields.List(fields.Nested(LocationBaseSchema), required=True, validate=validate.Length(min=1))

class ProgramQualificationSchema(Schema):
    qualifications = fields.List(fields.Nested(QualificationSchema), required=True, validate=validate.Length(min=1))

class ProgramCategorySchema(Schema):
    category_ids = fields.List(fields.Str(validate=validate.Length(equal=36)), required=True, validate=validate.Length(min=1))