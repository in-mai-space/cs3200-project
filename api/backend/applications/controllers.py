from typing import Any, Dict, Tuple
from flask import Blueprint, request, jsonify, Response
from marshmallow import ValidationError
from backend.validators.applications import ApplicationSchema
from backend.applications.transactions import (
    get_application_by_id,
    insert_application,
    update_application,
    delete_application
)
from backend.utilities.errors import handle_error
from backend.utilities.uuid import validate_uuid
from http import HTTPStatus

applications = Blueprint('applications', __name__)

@applications.route('/programs/<string:program_id>/applications', methods=['POST'], strict_slashes=False)
def create_application(program_id: str) -> Tuple[Any, int]:
    try:
        validate_uuid(program_id)

        schema = ApplicationSchema()
        payload = schema.load(request.json)
        result = insert_application(program_id, payload)

        return jsonify(result), HTTPStatus.CREATED

    except Exception as e:
        return handle_error(e)
    
@applications.route('/<string:application_id>', methods=['GET'])
def get_application_route(application_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(application_id)
        result = get_application_by_id(application_id)
        return jsonify(result), HTTPStatus.OK
    except Exception as e:
        return handle_error(e)

@applications.route('/<string:application_id>', methods=['PUT'], strict_slashes=False)
def update_application_route(application_id: str) -> Tuple[Any, int]:
    try:
        validate_uuid(application_id)

        schema = ApplicationSchema()
        payload = schema.load(request.json)
        result = update_application(application_id, payload)

        return jsonify(result), HTTPStatus.OK

    except ValidationError as ve:
        return handle_error(ve)

    except Exception as e:
        return handle_error(e)


# DELETE endpoint: Delete an application.
@applications.route('/<string:application_id>', methods=['DELETE'])
def delete_application_route(application_id: str) -> tuple[Response, int]:
    try:
        # Validate that the provided application_id is a valid UUID.
        validate_uuid(application_id)
        
        # Delete the application.
        delete_application(application_id)
        return jsonify({"message": "Application deleted successfully"}), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)
