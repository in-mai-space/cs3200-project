from typing import Dict, Any, Tuple
from flask import Blueprint, request, jsonify, Response
from marshmallow import ValidationError
from backend.users.validators import UserSchema
from backend.users.transactions import (
    insert_user
)
from backend.utilities.errors import handle_error
from backend.utilities.uuid import validate_uuid
from http import HTTPStatus

users = Blueprint('users', __name__)

# Tony's code ========================================================
# Create a user
@users.route('/', methods=['POST'], strict_slashes=False)
def create_user() -> Tuple[Any, int]:
    try:
        # Validate the request body (using a schema if available)
        # For example, using Marshmallow you might do:
        user_schema = UserSchema()  # Ensure you have defined a proper schema for user data.
        data = user_schema.load(request.json)

        # Insert the user record into the database.
        result = insert_user(data)
        return jsonify(result), HTTPStatus.CREATED

    except Exception as e:
        # Centralized error handling; you might have a dedicated error handler function.
        return handle_error(e)