from typing import Dict, Any, Tuple
from flask import Blueprint, request, jsonify, Response
from marshmallow import ValidationError
from backend.users.validators import UserSchema, UserUpdateSchema
from backend.users.transactions import (
    delete_user,
    get_user_by_id,
    insert_user,
    update_user
)
from backend.database import db
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
    
@users.route('/<string:user_id>', methods=['DELETE'])
def delete_user_route(user_id: str) -> Tuple[Response, int]:
    try:
        # Validate that the provided user_id is a valid UUID.
        validate_uuid(user_id)

        # Delete user from the database using the helper function.
        delete_user(user_id)
        return jsonify({"message": "User deleted successfully"}), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)