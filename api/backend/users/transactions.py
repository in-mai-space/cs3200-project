from typing import Dict, List, Any

from flask import jsonify
from backend.database import db
from backend.utilities.errors import DatabaseError, ConflictError, NotFoundError
from mysql.connector import Error as MySQLError

# Tony's code ========================================================
def insert_user(data: Dict[str, str]) -> Dict[str, Any]:
    """
    Insert a new user record into the database.

    Args:
        data (Dict[str, str]): A dictionary containing the user's data.
            Must include 'first_name', 'last_name', and 'type'.

    Returns:
        Dict[str, Any]: The newly created user record.

    Raises:
        DatabaseError: If an error occurs during user creation.
    """
    cursor = db.get_db().cursor()
    try: 
        cursor.execute('INSERT INTO users (first_name, last_name, type) VALUES (%s, %s, %s)', (data['first_name'], data['last_name'], data['type']))
        db.get_db().commit()
        return {"message": "User created successfully"}
    except Exception as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def get_user_by_id(user_id: str) -> Dict[str, Any]:
    """
    Fetch the user record from the database by user id.

    Args:
        user_id (str): The unique identifier of the user.

    Returns:
        Dict[str, Any]: The user record if found.

    Raises:
        DatabaseError: If there's an error fetching the user.
    """
    cursor = db.get_db().cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if not result:
            raise DatabaseError("User not found")
        return result
    except MySQLError as e:
        raise DatabaseError(f"Error fetching user: {str(e)}")
    finally:
        cursor.close()