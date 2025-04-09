from typing import Dict, List, Any
from backend.database import db
from backend.utilities.errors import DatabaseError, ConflictError, NotFoundError
from mysql.connector import Error as MySQLError

def create_category(data: Dict[str, str]) -> Dict[str, Any]:
    cursor = db.get_db().cursor()
    try: 
        cursor.execute('INSERT INTO categories (name) VALUES (%s)', (data['name'],))
        db.get_db().commit()
        cursor.execute('SELECT * FROM categories WHERE name = %s', (data['name'],))
        result = cursor.fetchone()
        if not result:
            raise DatabaseError("Failed to create category")
        return result
    except MySQLError as e:
        if e.args[0] == 1062:
            raise ConflictError(f"Category with name {data['name']} already exists")
        else:
            raise DatabaseError(str(e))
    finally:
        cursor.close()

def get_all_categories(page: int, limit: int) -> List[Dict[str, Any]]:
    cursor = db.get_db().cursor()
    try:
        offset = (page - 1) * limit
        cursor.execute('SELECT * FROM categories ORDER BY name LIMIT %s OFFSET %s', (limit, offset))
        return cursor.fetchall()
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def get_category_by_id(category_id: str) -> Dict[str, Any]:
    cursor = db.get_db().cursor()
    try:
        cursor.execute('SELECT * FROM categories WHERE id = %s', (category_id,))
        result = cursor.fetchone()
        if not result:
            raise NotFoundError(f"Category with id {category_id} does not exist")
        return result
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def update_category(category_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
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
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM categories WHERE id = %s', (category_id,))
        db.get_db().commit()
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()
