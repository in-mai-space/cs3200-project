from typing import Dict, Any, Optional, Tuple
from flask import jsonify, Response
from http import HTTPStatus
from marshmallow.exceptions import ValidationError as MarshmallowValidationError

class CustomAPIError(Exception):
    """Base class for custom API errors."""
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    message = "An unexpected error occurred"

    def __init__(self, message: Optional[str] = None, status_code: Optional[int] = None):
        self.message = message or self.__class__.message
        self.status_code = status_code or self.__class__.status_code
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary format."""
        return {
            "error": {
                "message": self.message,
                "status": self.status_code,
                "type": self.__class__.__name__
            }
        }

class DatabaseError(CustomAPIError):
    """Raised when a database operation fails."""
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    message = "A database error occurred"

class ValidationError(CustomAPIError):
    """Raised when data validation fails."""
    status_code = HTTPStatus.BAD_REQUEST
    message = "Invalid data provided"

class NotFoundError(CustomAPIError):
    """Raised when a requested resource is not found."""
    status_code = HTTPStatus.NOT_FOUND
    message = "Resource not found"

class ConflictError(CustomAPIError):
    """Raised when there is a conflict with existing data."""
    status_code = HTTPStatus.CONFLICT
    message = "Resource already exists"

class ForbiddenError(CustomAPIError):
    """Raised when user doesn't have permission."""
    status_code = HTTPStatus.FORBIDDEN
    message = "Permission denied"

def handle_error(error: Exception) -> Tuple[Response, int]:
    """Handle different types of errors and return appropriate responses."""
    if isinstance(error, CustomAPIError):
        return jsonify(error.to_dict()), error.status_code
    
    if isinstance(error, MarshmallowValidationError):
        return jsonify({
            "error": {
                "message": error.messages,
                "type": "ValidationError"
            }
        }), HTTPStatus.BAD_REQUEST
    
    # Handle unexpected errors
    return jsonify({
        "error": {
            "message": str(error),
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
            "type": "UnexpectedError"
        }
    }), HTTPStatus.INTERNAL_SERVER_ERROR
    
    
    