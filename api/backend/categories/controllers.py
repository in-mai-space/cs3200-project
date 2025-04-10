from backend.utilities.pagination import validate_pagination
from flask import Blueprint, request, jsonify, Response
from backend.validators.categories import CategorySchema, CategoryUpdateSchema
from backend.categories.transactions import (
    create_category,
    get_all_categories,
    get_category_by_id,
    update_category,
    delete_category
)
from backend.utilities.errors import handle_error
from backend.utilities.uuid import validate_uuid
from http import HTTPStatus

categories = Blueprint('categories', __name__)

#------------------------------------------------------------
# Create a category
@categories.route('', methods=['POST'], strict_slashes=False)
def create_categories() -> tuple[Response, int]:
    try:
        category_schema = CategorySchema()
        data = category_schema.load(request.json)
        result = create_category(data)
        return jsonify(result), HTTPStatus.CREATED

    except Exception as e:
        return handle_error(e)

#------------------------------------------------------------
# Get all available categories with page and limit (pagination)
@categories.route('', methods=['GET'], strict_slashes=False)
def get_categories() -> tuple[Response, int]:
    try:
        page, limit = validate_pagination()
        categories = get_all_categories(page=page, limit=limit)
        return jsonify(categories), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)

#------------------------------------------------------------
# Get a specific category
@categories.route('/<string:category_id>', methods=['GET'])
def get_category(category_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(category_id)
        category = get_category_by_id(category_id)
        return jsonify(category), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)

#------------------------------------------------------------
# Update a specific category
@categories.route('/<string:category_id>', methods=['PUT'])
def update_category_route(category_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(category_id)
        category_schema = CategoryUpdateSchema()
        data = category_schema.load(request.json)
        result = update_category(category_id, data)
        return jsonify(result), HTTPStatus.OK

    except Exception as e:
        return handle_error(e)

#------------------------------------------------------------
# Delete a specific category
@categories.route('/<string:category_id>', methods=['DELETE'])
def delete_category_route(category_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(category_id)
        delete_category(category_id)
        return jsonify({"message": "Category deleted successfully"}), HTTPStatus.OK
        
    except Exception as e:
        return handle_error(e)