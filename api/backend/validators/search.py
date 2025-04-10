from backend.utilities.uuid import validate_uuid
from flask import request
from backend.utilities.pagination import validate_pagination
from marshmallow import Schema, fields, validates, ValidationError, validate

class SearchQueryParamSchema(Schema):
    search_query = fields.Str(allow_none=True)
    page = fields.Int(allow_none=True)
    limit = fields.Int(allow_none=True)
    user_id = fields.Str(allow_none=True)
    categories = fields.List(fields.Str(), allow_none=True)
    location = fields.Dict(keys=fields.Str(), values=fields.Str(), allow_none=True)
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
        if value is None:
            return
        allowed_fields = {"city", "state", "zip_code", "country"}
        if not all(k in allowed_fields for k in value):
            raise ValidationError("Invalid location field")

    @validates("categories")
    def validate_categories(self, value):
        if not all(isinstance(cat, str) for cat in value):
            raise ValidationError("Categories must be strings")
    

def validate_search_params():
    """
    Validates and processes search query parameters from the request.
    Returns a tuple of (page, limit, validated_search_params)
    """
    page, limit = validate_pagination()
    user_id = request.args.get('user_id')
    if user_id:
        validate_uuid(user_id)

    # Build location dictionary only if any location parameters are present
    location = None
    location_params = ['city', 'state', 'zip_code', 'country']
    if any(request.args.get(loc) for loc in location_params):
        location = {
            'city': request.args.get('city'),
            'state': request.args.get('state'),
            'zip_code': request.args.get('zip_code'),
            'country': request.args.get('country')
        }
        location = {k: v for k, v in location.items() if v is not None}
        if not location:
            location = None

    query_params = {
        'search_query': request.args.get('search_query'),
        'categories': request.args.getlist('categories') or [],
        'user_id': user_id or None,
        'sort_by': request.args.get('sort_by', 'name'),
        'sort_order': request.args.get('sort_order', 'asc'),
        'page': page,
        'limit': limit,
        'location': location
    }

    schema = SearchQueryParamSchema()
    try:
        validated_params = schema.load(query_params)
    except ValidationError as err:
        raise ValidationError(f"Invalid query parameters: {err.messages}")

    return validated_params
