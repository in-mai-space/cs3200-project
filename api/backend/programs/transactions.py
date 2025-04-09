from typing import Dict, List, Any
from backend.database import db
from backend.utilities.errors import DatabaseError, ConflictError, NotFoundError
from mysql.connector import Error as MySQLError
