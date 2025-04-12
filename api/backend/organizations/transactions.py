from typing import Dict, Any, List, Optional
from backend.programs.transactions import retrieve_program
from backend.database import db
from backend.utilities.errors import ConflictError, DatabaseError, NotFoundError, ValidationError
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

def create_organization(data: Dict[str, str]) -> Dict[str, Any]:
    cursor = db.get_db().cursor()
    try: 
        cursor.execute('INSERT INTO organizations (name, description, website_url) VALUES (%s, %s, %s)', 
                       (data['name'], data['description'], data['website_url']))
        db.get_db().commit()
        cursor.execute('SELECT * FROM organizations WHERE name = %s', (data['name'],))
        result = cursor.fetchone()
        if not result:
            raise DatabaseError("Failed to create organization")
        return result
    except MySQLError as e:
        if e.args[0] == 1062:
            raise ConflictError(f"Organization with name {data['name']} already exists")
        else:
            raise DatabaseError(str(e))
    finally:
        cursor.close()


def get_organization_by_id(organization_id: str):
    cursor = db.get_db().cursor()
    try:
        cursor.execute('SELECT * FROM organizations WHERE id = %s', (organization_id,))
        result = cursor.fetchone()
        if not result:
            raise NotFoundError(f"Organization with id {organization_id} does not exist")
        return result
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def update_organization_by_id(organization_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    cursor = db.get_db().cursor()
    try: 
        update_fields = []
        values = []
        for key in ['name, description, website_url, is_verified']:
            if key in update_data:
                update_fields.append(f"{key} = %s")
                values.append(update_data[key])
        if not update_fields:
            raise DatabaseError("No valid fields to update")
        values.append(organization_id)
        query = f"UPDATE organization SET {', '.join(update_fields)} WHERE id = %s"
        cursor.execute(query, values)
        db.get_db().commit()

         # Fetch the updated organization
        cursor.execute('SELECT * FROM categories WHERE id = %s', (organization_id,))
        result = cursor.fetchone()
        if not result:
            raise NotFoundError(f"Organization with id {organization_id} does not exist")
        return result
    except MySQLError as e:
        if e.args[0] == 1062:
            raise ConflictError(f"Organization with name {update_data['name']} already exists")
        else:
            raise DatabaseError(str(e))
    finally:
        cursor.close()
        

    
        
def delete_organization_by_id(organization_id: str):
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM organizations WHERE id = %s', (organization_id))
        db.get_db().commit()
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()