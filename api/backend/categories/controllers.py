from typing import Tuple
from flask import Blueprint, request, jsonify, Response
from backend.validators.categories import CategorySchema, CategoryUpdateSchema
from backend.categories.transactions import (
    create_category,
    get_all_categories,
    get_category_by_id,
    update_category,
    delete_category
)
from backend.utilities.errors import handle_error, BadRequestError
from backend.utilities.uuid import validate_uuid
from http import HTTPStatus

categories = Blueprint('categories', __name__)

#------------------------------------------------------------
# Create a category
@categories.route('', methods=['POST'], strict_slashes=False)
def create_categories() -> Tuple[Response, int]:
    try:
        # validate request body
        category_schema = CategorySchema()
        data = category_schema.load(request.json)
        
        # create category using transaction
        result = create_category(data)
        return jsonify(result), HTTPStatus.CREATED

    except Exception as e:
        return handle_error(e)

#------------------------------------------------------------
# Get all available categories with page and limit (pagination)
@categories.route('', methods=['GET'], strict_slashes=False)
def get_categories() -> Tuple[Response, int]:
    try:
        # get the query params for pagination
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=10, type=int)

        # validate that page and limit are positive integers
        if page <= 0 or limit <= 0:
            raise BadRequestError("Page and limit must be positive integers.")

        # fetch categories with pagination
        categories = get_all_categories(page=page, limit=limit)
        return jsonify(categories), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)

#------------------------------------------------------------
# Get a specific category
@categories.route('/<string:category_id>', methods=['GET'])
def get_category(category_id: str) -> Tuple[Response, int]:
    try:
        # validate if it is a valid UUID
        validate_uuid(category_id)

        category = get_category_by_id(category_id)
        return jsonify(category), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)

#------------------------------------------------------------
# Update a specific category
@categories.route('/<string:category_id>', methods=['PUT'])
def update_category_route(category_id: str) -> Tuple[Response, int]:
    try:
        # validate if it is a valid UUID
        validate_uuid(category_id)
        
        # validate request body
        category_schema = CategoryUpdateSchema()
        data = category_schema.load(request.json)
        
        # update category using transaction
        result = update_category(category_id, data)
        return jsonify(result), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)

#------------------------------------------------------------
# Delete a specific category
@categories.route('/<string:category_id>', methods=['DELETE'])
def delete_category_route(category_id: str) -> Tuple[Response, int]:
    try:
        # validate if it is a valid UUID
        validate_uuid(category_id)

        # delete from database
        result = delete_category(category_id)
        return jsonify({"message": "Category deleted successfully"}), HTTPStatus.OK
        
    except Exception as e:
        return handle_error(e)