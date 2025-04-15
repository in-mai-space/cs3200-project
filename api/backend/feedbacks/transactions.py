from backend.database import db
from backend.utilities.errors import DatabaseError, NotFoundError
from mysql.connector import Error as MySQLError
from typing import Dict, Any

def create_feedback(program_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    cursor = db.get_db().cursor()
    try:
        query = '''
            INSERT INTO feedbacks (program_id, user_id, rating, comment)
            VALUES (%s, %s, %s, %s)
        '''
        values = (program_id, data['user_id'], data['rating'], data['comment'])
        cursor.execute(query, values)
        db.get_db().commit()
        feedback_id = cursor.lastrowid

        cursor.execute('SELECT * FROM feedbacks WHERE id = %s', (feedback_id,))
        result = cursor.fetchone()
        return result

    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def get_feedback_by_id(feedback_id: str) -> Dict[str, Any]:
    cursor = db.get_db().cursor()
    try:
        cursor.execute('SELECT * FROM feedbacks WHERE id = %s', (feedback_id,))
        result = cursor.fetchone()
        if not result:
            raise NotFoundError(f"Feedback with ID {feedback_id} not found")
        return result
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def delete_feedback(feedback_id: str) -> None:
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM feedbacks WHERE id = %s', (feedback_id,))
        db.get_db().commit()
        if cursor.rowcount == 0:
            raise NotFoundError(f"No feedback with ID {feedback_id} to delete")
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()
