from http import HTTPStatus
from typing import Tuple
from api.backend.utilities.errors import handle_error
from api.backend.utilities.uuid import validate_uuid
from api.backend.validators.programs import ProgramSchema
from flask import Blueprint, request, jsonify, Response

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
organizations = Blueprint('organizations', __name__)

#------------------------------------------------------------
# Create a program for an organization
@organizations.route('/<string:id>/programs', methods=['POST'])
def create_program(id: str) -> Tuple[Response, int]:
    try:
        # validate if it is a valid UUID
        validate_uuid(id)

        # validate request body
        program_schema = ProgramSchema()
        data = program_schema.load(request.json)

        # create program using transaction
        result = insert_program(data)
        return jsonify(result), HTTPStatus.CREATED
    
    except Exception as e:
        return handle_error(e)