from backend.database import db
from backend.utilities.errors import DatabaseError, NotFoundError
from mysql.connector import Error as MySQLError
from typing import Dict, Any

def create_application(program_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    cursor = db.get_db().cursor()
    try:
        query = '''
            INSERT INTO applications (program_id, user_id, status, notes)
            VALUES (%s, %s, %s, %s)
        '''
        values = (program_id, data['user_id'], data['status'], data['notes'])
        cursor.execute(query, values)
        db.get_db().commit()
        application_id = cursor.lastrowid

        cursor.execute('SELECT * FROM applications WHERE id = %s', (application_id,))
        result = cursor.fetchone()
        return result

    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

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
    cursor = db.get_db().cursor()
    try:
        query = '''
            UPDATE applications
            SET status = %s, notes = %s
            WHERE id = %s
        '''
        values = (data['status'], data['notes'], application_id)
        cursor.execute(query, values)
        db.get_db().commit()

        cursor.execute('SELECT * FROM applications WHERE id = %s', (application_id,))
        result = cursor.fetchone()
        if not result:
            raise NotFoundError(f"Application with ID {application_id} not found")
        return result

    except MySQLError as e:
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
