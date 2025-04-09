from backend.utilities.errors import ValidationError
from flask import request

def validate_pagination() -> tuple[int, int]:
    """
    Validate pagination parameters in the query string of a GET request.

    This function retrieves the `page` and `limit` query parameters, 
    defaults them to `1` and `10` respectively if not provided, 
    and raises a `ValidationError` if either parameter is less than or equal to 0.
    """
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)

    if page <= 0 or limit <= 0:
        raise ValidationError("Page and limit must be positive integers.")
    
    return page, limit
