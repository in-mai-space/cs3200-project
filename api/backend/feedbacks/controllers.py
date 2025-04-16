from flask import Blueprint, request, jsonify, Response
from backend.feedbacks.transactions import (
    get_feedback_by_id,
    delete_feedback
)
from backend.utilities.errors import handle_error
from backend.utilities.uuid import validate_uuid
from http import HTTPStatus

feedbacks = Blueprint('feedbacks', __name__)

@feedbacks.route('/<string:feedback_id>', methods=['GET'])
def get_feedback_route(feedback_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(feedback_id)
        result = get_feedback_by_id(feedback_id)
        return jsonify(result), HTTPStatus.OK
    except Exception as e:
        return handle_error(e)

@feedbacks.route('/<string:feedback_id>', methods=['DELETE'])
def delete_feedback_route(feedback_id: str) -> tuple[Response, int]:
    try:
        validate_uuid(feedback_id)
        delete_feedback(feedback_id)
        return jsonify({'message': 'Feedback deleted successfully'}), HTTPStatus.OK
    except Exception as e:
        return handle_error(e)
