from typing import Dict, List, Any
from unittest import result

from flask import jsonify
from backend.database import db
from backend.utilities.errors import DatabaseError, ConflictError, NotFoundError
from mysql.connector import Error as MySQLError

def insert_point_of_contact(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Insert a new point of contact record into the database.

    Args:
        data (Dict[str, Any]): A dictionary containing the point of contact data.
            Must include 'contact_type', 'entity_id', and 'email'.
            Optionally include 'description' and 'phone_number'.

    Returns:
        Dict[str, Any]: A message confirming the successful creation of the point of contact.

    Raises:
        DatabaseError: If an error occurs during the insertion.
    """
    cursor = db.get_db().cursor()
    try:
        # Retrieve optional fields or default to None
        description = data.get('description')
        phone_number = data.get('phone_number')
        cursor.execute(
            "INSERT INTO point_of_contacts (contact_type, entity_id, description, email, phone_number) VALUES (%s, %s, %s, %s, %s)",
            (data['contact_type'], data['entity_id'], description, data['email'], phone_number)
        )
        db.get_db().commit()
        return {"message": "Point of contact created successfully"}
    except Exception as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def get_point_of_contact_by_id(contact_id: str) -> Dict[str, Any]:
    """
    Fetch the point of contact record from the database by its ID.

    Args:
        contact_id (str): The unique identifier of the point of contact.

    Returns:
        Dict[str, Any]: The point of contact record if found.

    Raises:
        DatabaseError: If there's an error fetching the point of contact.
    """
    cursor = db.get_db().cursor()
    try:
        cursor.execute("SELECT * FROM point_of_contacts WHERE id = %s", (contact_id,))
        result = cursor.fetchone()
        if not result:
            raise DatabaseError("Point of contact not found")
        return result
    except MySQLError as e:
        raise DatabaseError(f"Error fetching point of contact: {str(e)}")
    finally:
        cursor.close()