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
        for key in ['name', 'description', 'website_url', 'is_verified']:
            if key in update_data:
                update_fields.append(f"{key} = %s")
                values.append(update_data[key])
        if not update_fields:
            raise DatabaseError("No valid fields to update")
        values.append(organization_id)
        query = f"UPDATE organizations SET {', '.join(update_fields)} WHERE id = %s"
        cursor.execute(query, values)
        db.get_db().commit()

         # Fetch the updated organization
        cursor.execute('SELECT * FROM organizations WHERE id = %s', (organization_id,))
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

def create_org_contact(organization_id: str, data: Dict[str, str]) -> Dict[str, Any]:
    cursor = db.get_db().cursor()
    try: 
        cursor.execute('INSERT INTO point_of_contacts (contact_type, entity_id, description, email, phone_number) VALUES (%s, %s, %s, %s, %s)', 
                       ('organization', organization_id, data['description'], data['email'], data['phone_number']))
        db.get_db().commit()
        cursor.execute('SELECT * FROM point_of_contacts WHERE id = %s', (cursor.lastrowid,))
        result = cursor.fetchone()
        if not result:
            raise DatabaseError("Failed to create organization contact")
        return result
    except MySQLError as e:
        if e.args[2] == 1062:
            raise ConflictError(f"Contact with description {data['description']} already exists")
        if e.args[3] == 1062:
            raise ConflictError(f"Contact with email {data['email']} already exists")
        if e.args[4] == 1062:
            raise ConflictError(f"Contact with phone number {data['phone_number']} already exists")
        else:
            raise DatabaseError(str(e))
    finally:
        cursor.close()

def update_org_contact(contact_id: str, data: Dict[str, str]) -> Dict[str, Any]:
    cursor = db.get_db().cursor()
    try: 
        update_fields = []
        values = []
        for key in ['description', 'email', 'phone_number']:
            if key in data:
                update_fields.append(f"{key} = %s")
                values.append(data[key])
        if not update_fields:
            raise DatabaseError("No valid fields to update")
        values.append(contact_id)
        query = f"UPDATE point_of_contacts SET {', '.join(update_fields)} WHERE id = %s"
        cursor.execute(query, values)
        db.get_db().commit()

         # Fetch the updated organization
        cursor.execute('SELECT * FROM point_of_contacts WHERE id = %s', (contact_id,))
        result = cursor.fetchone()
        if not result:
            raise NotFoundError(f"Contact with id {contact_id} does not exist")
        return result
    except MySQLError as e:
        if e.args[2] == 1062:
            raise ConflictError(f"Contact with description {data['description']} already exists")
        if e.args[3] == 1062:
            raise ConflictError(f"Contact with email {data['email']} already exists")
        if e.args[4] == 1062:
            raise ConflictError(f"Contact with phone number {data['phone_number']} already exists")
        else:
            raise DatabaseError(str(e))
    finally:
        cursor.close()


def get_organization_contact(org_contact_id: str):
    cursor = db.get_db().cursor()
    try:
        cursor.execute('SELECT * FROM point_of_contacts WHERE id = %s', (org_contact_id,))
        result = cursor.fetchone()
        if not result:
            raise NotFoundError(f"Organization contact with id {org_contact_id} does not exist")
        return result
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def delete_organization_contact(org_contact_id: str):
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM point_of_contacts WHERE id = %s', (org_contact_id))
        db.get_db().commit()
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def search_org(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    cursor = db.get_db().cursor()
    try:
        # First get basic organization data
        query = """
            SELECT 
                o.id, 
                o.name, 
                o.description, 
                o.website_url
            FROM organizations o
            ORDER BY o.name ASC
            LIMIT %s OFFSET %s
        """
        # Handle pagination
        page = params.get('page', 1)
        limit = params.get('limit', 10)
        offset = (page - 1) * limit
        query_params = [limit, offset]

        cursor.execute(query, query_params)
        results = cursor.fetchall()
        
        # Convert to list of dictionaries
        organizations = [dict(row) for row in results]
        
        # For each organization, get its categories and locations
        for org in organizations:
            # Get categories
            cursor.execute("""
                SELECT c.id, c.name 
                FROM categories c
                JOIN organization_categories oc ON c.id = oc.category_id
                WHERE oc.organization_id = %s
            """, (org['id'],))
            org['categories'] = [dict(row) for row in cursor.fetchall()]
            
            # Get locations
            cursor.execute("""
                SELECT id, location_type, type, address_line1, address_line2, 
                       city, state, zip_code, country, is_primary
                FROM locations
                WHERE entity_id = %s AND location_type = 'organization'
            """, (org['id'],))
            org['locations'] = [dict(row) for row in cursor.fetchall()]

        return organizations

    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()





