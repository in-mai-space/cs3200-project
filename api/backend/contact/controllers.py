from typing import Dict, Any, Tuple
from flask import Blueprint, request, jsonify, Response
from marshmallow import ValidationError
from backend.contact.transactions import get_point_of_contact_by_id, insert_point_of_contact
from backend.contact.validators import PointOfContactSchema
from backend.users.validators import UserSchema, UserUpdateSchema
from backend.database import db
from backend.utilities.errors import NotFoundError, handle_error
from backend.utilities.uuid import validate_uuid
from http import HTTPStatus

contact = Blueprint('contact', __name__)

@contact.route('/', methods=['POST'], strict_slashes=False)
def create_point_of_contact() -> Tuple[Any, int]:
    try:
        # Validate the request body using the point of contact schema
        poc_schema = PointOfContactSchema()
        data = poc_schema.load(request.json)

        # Insert the point of contact record into the database.
        result = insert_point_of_contact(data)
        return jsonify(result), HTTPStatus.CREATED

    except Exception as e:
        return handle_error(e)

# GET endpoint for retrieving a point of contact by ID
@contact.route('/<contact_id>', methods=['GET'], strict_slashes=False)
def get_point_of_contact(contact_id: str) -> Tuple[Any, int]:
    try:
        # Fetch the point of contact record using the refactored helper function
        result = get_point_of_contact_by_id(contact_id)
        return jsonify(result), HTTPStatus.OK
    except Exception as e:
        return handle_error(e)