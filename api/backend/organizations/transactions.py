from typing import Dict, Any
from backend.database import db
from backend.utilities.errors import DatabaseError, ConflictError, NotFoundError
from mysql.connector import Error as MySQLError

def create_program(data: Dict[str, str]) -> Dict[str, Any]:
    cursor = db.get_db().cursor()
    try:
        cursor.execute('INSERT INTO programs (name, description, status, start_date, deadline, organization_id, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s)', (data['name'], data['description'], data['status'], data['start_date'], data['deadline'], data['organization_id'], data['category_id']))
        db.get_db().commit()
        return cursor.lastrowid
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()