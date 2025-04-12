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