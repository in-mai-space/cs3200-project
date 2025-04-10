from http import HTTPStatus
from backend.organizations.transactions import insert_program
from backend.utilities.errors import handle_error
from backend.utilities.uuid import validate_uuid
from flask import Blueprint, request, jsonify, Response
from backend.validators.programs import ProgramCreateSchema

organizations = Blueprint('organizations', __name__)

#------------------------------------------------------------
# Create a program for an organization
@organizations.route('/<string:id>/programs', methods=['POST'])
def create_program(id: str) -> tuple[Response, int]:
    try:
        validate_uuid(id)

        program_schema = ProgramCreateSchema()
        data = program_schema.load(request.json)

        insert_program(id, data)
        return jsonify({ "message": "Program created successfully" }), HTTPStatus.CREATED
    
    except Exception as e:
        return handle_error(e)