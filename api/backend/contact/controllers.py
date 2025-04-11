from typing import Dict, Any, Tuple
from flask import Blueprint, request, jsonify, Response
from marshmallow import ValidationError
from backend.users.validators import UserSchema, UserUpdateSchema
from backend.users.transactions import (
    delete_user,
    get_user_by_id,
    insert_user,
    update_user
)
from backend.database import db
from backend.utilities.errors import NotFoundError, handle_error
from backend.utilities.uuid import validate_uuid
from http import HTTPStatus

users = Blueprint('users', __name__)

