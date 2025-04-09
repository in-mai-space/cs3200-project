from typing import Dict, List, Any
from backend.database import db
from backend.utilities.errors import DatabaseError, ConflictError, NotFoundError
from mysql.connector import Error as MySQLError
from backend.utilities.uuid import validate_uuid
from backend.validators.programs import ProgramSchema

def create_program(data: Dict[str, str]) -> Dict[str, Any]:
    """
    Create a new program in the database.

    Args:
        data (Dict[str, str]): Dictionary containing the program data.
            Must contain a 'name' key with the program name.

    Returns:
        Dict[str, Any]: The created program.

    Raises:
        ConflictError: If a program with the same name already exists.
        DatabaseError: If there's an error creating the program.
    """
    cursor = db.get_db().cursor()
    try:
        cursor.execute('INSERT INTO programs (name, description, status, start_date, deadline, organization_id, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s)', (data['name'], data['description'], data['status'], data['start_date'], data['deadline'], data['organization_id'], data['category_id']))
        db.get_db().commit()
        return cursor.lastrowid
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()