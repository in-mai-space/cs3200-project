from typing import Dict, Any, Tuple
from flask import Blueprint, request, jsonify, Response
from marshmallow import ValidationError
from backend.user_profiles.transactions import get_user_profile_by_id, insert_user_profile
from backend.user_profiles.validators import UserProfileSchema
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