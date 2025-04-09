from flask import Blueprint, request, jsonify
from flask import make_response
from flask import current_app
from backend.database import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
organizations = Blueprint('organizations', __name__)

#------------------------------------------------------------
# Create a program for an organization
@organizations.route('/<string:id>/programs', methods=['POST'])
def create_program(id: str):
    try:
        # validate if it is a valid UUID
        validate_uuid(id)

        # validate request body
        program_schema = ProgramSchema()
        data = program_schema.load(request.json)

        # create program using transaction
        result = create_program(id)
        return jsonify(result), HTTPStatus.CREATED
    
    except Exception as e:
        return handle_error(e)