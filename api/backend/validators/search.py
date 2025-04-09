from flask import request
from api.backend.validators.search import SearchQueryParamSchema  # update path if needed
from api.backend.utilities.pagination import validate_pagination
from marshmallow import ValidationError

def validate_search_params():
    """
    Validates and processes search query parameters from the request.
    Returns a tuple of (page, limit, validated_search_params)
    """
    page, limit = validate_pagination()

    query_params = {
        'search_query': request.args.get('search_query'),
        'categories': request.args.getlist('categories') or None,
        'location': {
            'city': request.args.get('city'),
            'state': request.args.get('state'),
            'zip_code': request.args.get('zip_code'),
            'country': request.args.get('country')
        } if any(request.args.get(loc) for loc in ['city', 'state', 'zip_code', 'country']) else None,
        'is_qualified': request.args.get('is_qualified'),
        'sort_by': request.args.get('sort_by', 'name'),
        'sort_order': request.args.get('sort_order', 'asc'),
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

    return page, limit, validated_params
