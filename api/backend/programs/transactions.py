from typing import Dict, List, Any
from backend.database import db
from backend.utilities.errors import DatabaseError, ConflictError, NotFoundError
from mysql.connector import Error as MySQLError

def get_program_by_id(program_id: str) -> Dict[str, Any]:
    """
    Retrieve a specific program by its ID.

    Args:
        program_id (str): The UUID of the category to retrieve.

    Returns:
        Dict[str, Any]: The program information.

    Raises:
        NotFoundError: If no program exists with the given ID.
        DatabaseError: If there's an error retrieving the program.
    """
    cursor = db.get_db().cursor()
    try:
        cursor.execute('SELECT * FROM programs WHERE id = %s', (category_id,))
        result = cursor.fetchone()
        if not result:
            raise NotFoundError(f"Program with id {category_id} does not exist")
        return result
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def update_category(category_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing category.

    Args:
        category_id (str): The UUID of the category to update.
        update_data (Dict[str, Any]): Dictionary containing the fields to update.
            Currently only supports updating the 'name' field.

    Returns:
        Dict[str, Any]: The updated category with its ID and name.

    Raises:
        NotFoundError: If no category exists with the given ID.
        ConflictError: If updating the name would conflict with an existing category.
        DatabaseError: If there's an error updating the category.
    """
    cursor = db.get_db().cursor()
    try:
        update_fields = []
        values = []
        for key in ['name']:
            if key in update_data:
                update_fields.append(f"{key} = %s")
                values.append(update_data[key])
        if not update_fields:
            raise DatabaseError("No valid fields to update")
        values.append(category_id)
        query = f"UPDATE categories SET {', '.join(update_fields)} WHERE id = %s"
        cursor.execute(query, values)
        db.get_db().commit()
        
        # Fetch the updated category
        cursor.execute('SELECT * FROM categories WHERE id = %s', (category_id,))
        result = cursor.fetchone()
        if not result:
            raise NotFoundError(f"Category with id {category_id} does not exist")
        return result
    except MySQLError as e:
        if e.args[0] == 1062:
            raise ConflictError(f"Category with name {update_data['name']} already exists")
        else:
            raise DatabaseError(str(e))
    finally:
        cursor.close()

def delete_category(category_id: str) -> Dict[str, Any]:
    """
    Delete a category from the database.

    Args:
        category_id (str): The UUID of the category to delete.

    Returns:
        Dict[str, Any]: The deleted category's data.

    Raises:
        DatabaseError: If there's an error deleting the category.
    """
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM categories WHERE id = %s', (category_id,))
        db.get_db().commit()
        return result
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()
