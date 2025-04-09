from backend.validators.programs import ProgramUpdateSchema
from backend.programs.transactions import get_program_app_stats, get_program_applications, get_program_feedback, get_program_profiles, get_program_retention, get_program_stats, get_program_trends, remove_program, retrieve_program, search_program, update_program_info
from backend.utilities.pagination import validate_pagination
from flask import Blueprint, request, jsonify
from backend.utilities.errors import handle_error
from backend.utilities.uuid import validate_uuid
from http import HTTPStatus
from typing import Response
from backend.validators.search import validate_search_params
from backend.utilities.errors import BadRequestError

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
programs = Blueprint('programs', __name__)

#------------------------------------------------------------
# Get a specific program
@programs.route('/<string:program_id>', methods=['GET'])
def get_program(program_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(program_id)
        program = retrieve_program(program_id)
        return jsonify(program), HTTPStatus.OK
    
    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Search for programs
@programs.route('/search', methods=['GET'])
def search() -> tuple[Response, int]:
    try:
        params = validate_search_params()
        programs = search_program(params)
        return jsonify(programs), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Get a specific program's feedback forms
@programs.route('/<string:program_id>/feedbacks', methods=['GET'])
def get_feedback(program_id: str) -> tuple[Response, int]:
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
def get_profiles(program_id: str) -> tuple[Response, int]:
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
def get_applications(program_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(program_id)
        page, limit = validate_pagination()
        program = get_program_applications(program_id, page, limit)
        return jsonify(program), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)

#------------------------------------------------------------
# Get the stats of feedbacks of the program
@programs.route('/<string:program_id>/feedbacks/stats', methods=['GET'])
def get_feedback_stats(program_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(program_id)
        program = get_program_stats(program_id)
        return jsonify(program), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Get the trends of applications over time
@programs.route('/trends', methods=['GET'])
def get_trends() -> tuple[Response, int]:
    try:
        page, limit = validate_pagination()
        program = get_program_trends(page, limit)
        return jsonify(program), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Get the trends of applications over time
@programs.route('/retentions', methods=['GET'])
def get_trends() -> tuple[Response, int]:
    try:
        page, limit = validate_pagination()
        program = get_program_retention(page, limit)
        return jsonify(program), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)
    
#------------------------------------------------------------
# Update a specific program
@programs.route('/<string:program_id>', methods=['PUT'])
def update_program(program_id) -> tuple[Response, int]:
    try:
        validate_uuid(program_id)
        program_schema = ProgramUpdateSchema()
        data = program_schema.load(request.json)
        updated_program = update_program_info(program_id, data)
        if updated_program:
            return jsonify(updated_program), HTTPStatus.OK  
        else:
            raise BadRequestError(f"Program with id {program_id} does not exist")
    
    except Exception as e:
        return handle_error(e)

#------------------------------------------------------------
# Delete a specific program
@programs.route('/<string:program_id>', methods=['DELETE'])
def delete_program(program_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(program_id)
        remove_program(program_id)
        return jsonify({"message": "Program deleted successfully"}), HTTPStatus.OK
    
    except Exception as e:
        return handle_error(e)