from typing import Any, Tuple
from flask import Blueprint, request, jsonify, Response
from backend.validators.users import UserSchema, UserUpdateSchema
from backend.users.transactions import (
    get_user_by_id,
    insert_user,
    update_user
)
from backend.utilities.errors import NotFoundError, handle_error
from backend.utilities.uuid import validate_uuid
from http import HTTPStatus

users = Blueprint('users', __name__)

# Tony's code ========================================================
# POST endpoint for creating a user
@users.route('/', methods=['POST'], strict_slashes=False)
def create_user() -> Tuple[Any, int]:
    try:
        # Validate the request body using a schema
        user_schema = UserSchema() 
        data = user_schema.load(request.json)

        # Insert the user record into the database.
        result = insert_user(data)
        return jsonify(result), HTTPStatus.CREATED

    except Exception as e:
        return handle_error(e)
    
# New GET endpoint for retrieving a user by id.
@users.route('/<string:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id: str) -> Tuple[Any, int]:
    try:
        # validating via user_id
        validate_uuid(user_id)

        # Retrieve the user record from the database.
        user = get_user_by_id(user_id)
        return jsonify(user), HTTPStatus.OK

    except NotFoundError as e:
        return handle_error(e)
    except Exception as e:
        return handle_error(e)
    
# New PUT endpoint for updating a user
@users.route('/<string:user_id>', methods=['PUT'], strict_slashes=False)
def update_user_route(user_id: str) -> Tuple[Response, int]:
    try:
        # Validate that the provided user_id is a valid UUID
        validate_uuid(user_id)
        
        # Validate the request body using the update schema
        user_schema = UserUpdateSchema()
        data = user_schema.load(request.json)
        
        # Update the user using the helper function
        result = update_user(user_id, data)
        return jsonify(result), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)