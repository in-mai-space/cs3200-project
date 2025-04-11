from typing import Dict, Any, Tuple
from flask import Blueprint, request, jsonify, Response
from marshmallow import ValidationError
from backend.utilities.uuid import validate_uuid
from backend.user_profiles.transactions import get_user_profile_by_id, insert_user_profile, update_user_profile
from backend.user_profiles.validators import UserProfileSchema, UserProfileUpdateSchema
from backend.utilities.errors import handle_error
from http import HTTPStatus

user_profiles = Blueprint('user_profiles', __name__)

# POST endpoint for creating a user profile
@user_profiles.route('', methods=['POST'], strict_slashes=False)
def create_user_profile() -> Tuple[Any, int]:
    try:
        # Validate the request body using the user profile schema
        profile_schema = UserProfileSchema() 
        data = profile_schema.load(request.json)

        # Insert the user profile record into the database.
        result = insert_user_profile(data)
        return jsonify(result), HTTPStatus.CREATED

    except Exception as e:
        return handle_error(e)

@user_profiles.route('/<string:user_id>', methods=['GET'], strict_slashes=False)
def get_user_profile(user_id: str):
    try:
        profile = get_user_profile_by_id(user_id)
        if profile is None:
            return jsonify({'message': 'User profile not found'}), HTTPStatus.NOT_FOUND
        return jsonify(profile), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)
    
@user_profiles.route('/<string:user_id>', methods=['PUT'], strict_slashes=False)
def update_user_profile_route(user_id: str) -> Tuple[Response, int]:
    try:
        # Validate that the provided user_id is a valid UUID
        validate_uuid(user_id)
        
        # Validate the request body using the new update schema
        profile_schema = UserProfileUpdateSchema()
        data = profile_schema.load(request.json)
        
        # Update the user profile using the helper function
        result = update_user_profile(user_id, data)
        return jsonify(result), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)