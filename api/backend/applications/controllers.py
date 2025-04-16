from flask import Blueprint, request, jsonify, Response
from backend.applications.transactions import (
    get_application_by_id,
    update_application,
    delete_application
)
from backend.utilities.errors import handle_error
from backend.utilities.uuid import validate_uuid
from http import HTTPStatus

applications = Blueprint('applications', __name__)

@applications.route('/<string:application_id>', methods=['GET'])
def get_application_route(application_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(application_id)
        result = get_application_by_id(application_id)
        return jsonify(result), HTTPStatus.OK
    except Exception as e:
        return handle_error(e)

@applications.route('/<string:application_id>', methods=['PUT'])
def update_application_route(application_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(application_id)
        data = request.get_json()
        result = update_application(application_id, data)
        return jsonify(result), HTTPStatus.OK
    except Exception as e:
        return handle_error(e)

@applications.route('/<string:application_id>', methods=['DELETE'])
def delete_application_route(application_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(application_id)
        delete_application(application_id)
        return jsonify({"message": "Application deleted successfully"}), HTTPStatus.OK
    except Exception as e:
        return handle_error(e)
