from backend.utilities.uuid import validate_uuid
from flask import request
from backend.utilities.pagination import validate_pagination
from marshmallow import Schema, fields, validates, ValidationError, validate

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


def validate_search_params():
    """
    Validates and processes search query parameters from the request.
    Returns a tuple of (page, limit, validated_search_params)
    """
    page, limit = validate_pagination()
    user_id = request.args.get('user_id')
    validate_uuid(user_id)

    query_params = {
        'search_query': request.args.get('search_query'),
        'categories': request.args.getlist('categories') or None,
        'user_id': user_id or None,
        'location': {
            'city': request.args.get('city'),
            'state': request.args.get('state'),
            'zip_code': request.args.get('zip_code'),
            'country': request.args.get('country')
        } if any(request.args.get(loc) for loc in ['city', 'state', 'zip_code', 'country']) else None,
        'is_qualified': request.args.get('is_qualified'),
        'sort_by': request.args.get('sort_by', 'name'),
        'sort_order': request.args.get('sort_order', 'asc'),
        'page': page,
        'limit': limit
    }

    # clean up location
    if query_params['location']:
        query_params['location'] = {k: v for k, v in query_params['location'].items() if v}
        if not query_params['location']:
            query_params['location'] = None

    # convert is_qualified to boolean if needed
    if query_params['is_qualified'] is not None:
        query_params['is_qualified'] = query_params['is_qualified'].lower() == 'true'

    schema = SearchQueryParamSchema()
    try:
        validated_params = schema.load(query_params)
    except ValidationError as err:
        raise ValueError(f"Invalid query parameters: {err.messages}")

    return validated_params
