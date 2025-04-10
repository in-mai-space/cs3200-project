from typing import Dict, Any, List, Optional
from backend.programs.transactions import retrieve_program
from backend.database import db
from backend.utilities.errors import DatabaseError, ValidationError
from mysql.connector import Error as MySQLError

def insert_program(organization_id: str, data: Dict[str, Any]) -> None:
    cursor = db.get_db().cursor()
    try:
        cursor.execute(
            'INSERT INTO programs (name, description, status, start_date, deadline, end_date, organization_id) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (data['name'], data['description'], data['status'], data['start_date'], data['deadline'], data.get('end_date'), organization_id)
        )
        db.get_db().commit()
        return None
    
    except MySQLError as e:
        db.get_db().rollback()
        raise DatabaseError(f"Database error: {str(e)} (Error code: {e.errno}, SQL State: {e.sqlstate})")
    except Exception as e:
        db.get_db().rollback()
        print(f"Unexpected error: {str(e)}")
        raise DatabaseError(f"Unexpected error: {str(e)}")
    finally:
        cursor.close()