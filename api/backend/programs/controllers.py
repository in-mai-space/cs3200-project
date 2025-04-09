from api.backend.utilities.pagination import validate_pagination
from flask import Blueprint, request, jsonify
from backend.utilities.errors import handle_error
from backend.utilities.uuid import validate_uuid
from http import HTTPStatus
from typing import Tuple, Response

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
programs = Blueprint('programs', __name__)

#------------------------------------------------------------
# Get a specific program
@programs.route('/<string:program_id>', methods=['GET'])
def get_program(program_id: str) -> Tuple[Response, int]:
    try:
        validate_uuid(program_id)
        program = retrieve_program(program_id)
        return jsonify(program), HTTPStatus.OK
    
    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Get a specific program
@programs.route('/search', methods=['GET'])
def search() -> Tuple[Response, int]:
    try:
        page, limit = validate_pagination()

        # TODO: handle validation of query params

        program = search_program(page, limit, categories, location, search_term, is_qualified, sort_by)

        return jsonify(program), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Get a specific program's feedback forms
@programs.route('/<string:program_id>/feedbacks', methods=['GET'])
def get_feedback(program_id: str) -> Tuple[Response, int]:
    try:
        validate_uuid(program_id)
        page, limit = validate_pagination()
        program = get_program_feedback(program_id, page, limit)
        return jsonify(program), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Get all user profiles who apply to specific program
@programs.route('/<string:program_id>/profiles', methods=['GET'])
def get_profiles(program_id: str) -> Tuple[Response, int]:
    try:
        validate_uuid(program_id)
        page, limit = validate_pagination()
        program = get_program_profiles(program_id, page, limit)
        return jsonify(program), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)

#------------------------------------------------------------
# Get all applications to a specific program
@programs.route('/<string:program_id>/applications', methods=['GET'])
def get_applications(program_id: str) -> Tuple[Response, int]:
    try:
        validate_uuid(program_id)
        page, limit = validate_pagination()
        program = get_program_applications(program_id, page, limit)
        return jsonify(program), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)

#------------------------------------------------------------
# Get the stats of how applications change over time
@programs.route('/<string:program_id>/applications/stats', methods=['GET'])
def get_applications_stats(program_id: str) -> Tuple[Response, int]:
    try:
        validate_uuid(program_id)
        page, limit = validate_pagination()
        program = get_program_app_stats(program_id, page, limit)
        return jsonify(program), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Get the retention of programs
@programs.route('/<string:program_id>/retention', methods=['GET'])
def get_retention(program_id: str) -> Tuple[Response, int]:
    try:
        validate_uuid(program_id)        # validate pagination params
        page, limit = validate_pagination()
        program = get_program_retention(program_id, page, limit)
        return jsonify(program), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Update a specific program
@programs.route('/<string:program_id>', methods=['PUT'])
def update_program(program_id):
    try:
        # TODO: add validation of request body here
        data = request.json
        updated_program = update_program_info(data)
        return jsonify(updated_program), HTTPStatus.OK
    
    except Exception as e:
        return handle_error(e)

#------------------------------------------------------------
# Delete a specific program
@programs.route('/<string:program_id>', methods=['DELETE'])
def delete_program(program_id: str):
    try:
        validate_uuid(program_id)
        remove_program(program_id)
        return jsonify({"message": "Program deleted successfully"}), HTTPStatus.OK
    
    except Exception as e:
        return handle_error(e)