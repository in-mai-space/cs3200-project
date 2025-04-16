import uuid
from backend.database import db
from backend.utilities.errors import DatabaseError, NotFoundError
from mysql.connector import Error as MySQLError
from typing import Dict, Any

def get_application_by_id(application_id: str) -> Dict[str, Any]:
    cursor = db.get_db().cursor()
    try:
        cursor.execute('SELECT * FROM applications WHERE id = %s', (application_id,))
        result = cursor.fetchone()
        if not result:
            raise NotFoundError(f"Application with ID {application_id} not found")
        return result
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def update_application(application_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update fields of an existing application.
    """
    cursor = db.get_db().cursor()
    try:
        query = """
        UPDATE applications
        SET
            user_id             = %s,
            status              = %s,
            qualification_status= %s,
            decision_date       = %s,
            decision_notes      = %s,
            last_updated        = CURRENT_TIMESTAMP
        WHERE id = %s
        """
        cursor.execute(query, (
            data['user_id'],
            data.get('status'),
            data.get('qualification_status'),
            data.get('decision_date'),
            data.get('decision_notes'),
            application_id
        ))
        if cursor.rowcount == 0:
            # no row matched that id
            raise DatabaseError(f"No application found with id {application_id}")
        db.get_db().commit()
        return {"message": "Application updated successfully"}
    except Exception as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def delete_application(application_id: str) -> None:
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM applications WHERE id = %s', (application_id,))
        db.get_db().commit()
        if cursor.rowcount == 0:
            raise NotFoundError(f"No application with ID {application_id} to delete")
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()
