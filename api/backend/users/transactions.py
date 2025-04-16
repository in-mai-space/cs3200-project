from typing import Dict, List, Any

from flask import jsonify
from backend.database import db
from backend.utilities.errors import DatabaseError, NotFoundError
from mysql.connector import Error as MySQLError


def get_users(page: int, limit: int) -> List[Dict[str, Any]]:
    cursor = db.get_db().cursor()
    try:
        cursor.execute('SELECT * FROM users LIMIT %s OFFSET %s', (limit, (page - 1) * limit))
        return cursor.fetchall()
    except MySQLError as e:
        raise DatabaseError(str(e))

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

def update_user(user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing user record in the database.

    Args:
        user_id (str): The UUID of the user to update.
        update_data (Dict[str, Any]): Dictionary containing the fields to update.
            Supported keys are 'first_name', 'last_name', and 'type'.

    Returns:
        Dict[str, Any]: The updated user record.

    Raises:
        NotFoundError: If no user exists with the given ID.
        DatabaseError: If there's an error updating the user.
    """
    cursor = db.get_db().cursor()
    try:
        update_fields = []
        values = []
        # Loop only over allowed keys:
        for key in ['first_name', 'last_name', 'type']:
            if key in update_data:
                update_fields.append(f"{key} = %s")
                values.append(update_data[key])
        if not update_fields:
            raise DatabaseError("No valid fields to update")
        # Append the user_id for the WHERE clause
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
        cursor.execute(query, values)
        db.get_db().commit()
        
        # Fetch the updated user record
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if not result:
            raise NotFoundError(f"User with id {user_id} does not exist")
        return result
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def delete_user(user_id: str) -> Dict[str, Any]:
    """
    Delete a user from the database.

    Args:
        user_id (str): The UUID of the user to delete.

    Returns:
        Dict[str, Any]: An empty dict or additional info if needed.

    Raises:
        DatabaseError: If there's an error deleting the user.
    """
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
        db.get_db().commit()
        # Return an empty dict to be consistent with a structure that could return additional details.
        return {}
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()