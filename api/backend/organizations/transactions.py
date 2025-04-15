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
        query = """
            SELECT 
                o.id, 
                o.name, 
                o.description, 
                o.website_url,
                GROUP_CONCAT(DISTINCT CONCAT(c.id, ':', c.name)) as categories,
                GROUP_CONCAT(DISTINCT CONCAT(l.id, ':', l.location_type, ':', l.type, ':', l.address_line1, ':', l.address_line2, ':', l.city, ':', l.state, ':', l.zip_code, ':', l.country, ':', l.is_primary)) as locations
            FROM organizations o
            INNER JOIN programs p ON o.id = p.organization_id
            LEFT JOIN program_categories pc ON p.id = pc.program_id
            LEFT JOIN categories c ON pc.category_id = c.id
            LEFT JOIN locations l ON p.id = l.entity_id AND l.location_type = 'organization'
            WHERE 1=1
            GROUP BY o.id, o.name, o.description, o.website_url
        """
        query_params = []

        # Handle search query if present
        if params.get('search_query'):
            query += " AND (o.name LIKE %s OR o.description LIKE %s OR o.website_url LIKE %s)"
            search_term = f"%{params['search_query']}%"
            query_params.extend([search_term, search_term, search_term])

        # Handle categories if present and not empty
        categories = params.get('categories', [])
        if categories:
            query += " AND c.id IN (%s)" % ','.join(['%s'] * len(categories))
            query_params.extend(categories)

        # Handle location if present and not None
        location = params.get('location')
        if location is not None:
            location_conditions = []
            if location.get('city'):
                location_conditions.append("l.city = %s")
                query_params.append(location['city'])
            if location.get('state'):
                location_conditions.append("l.state = %s")
                query_params.append(location['state'])
            if location.get('zip_code'):
                location_conditions.append("l.zip_code = %s")
                query_params.append(location['zip_code'])
            if location.get('country'):
                location_conditions.append("l.country = %s")
                query_params.append(location['country'])
            
            if location_conditions:
                query += " AND (" + " OR ".join(location_conditions) + ")"
            else:
                # If no location conditions were added, we need to ensure we only get programs with locations
                query += " AND l.id IS NOT NULL"

        # Handle sorting
        sort_field = params.get('sort_by', 'created_at')
        sort_order = params.get('sort_order', 'DESC')
        query += f" ORDER BY o.{sort_field} {sort_order}"

        # Handle pagination
        page = params.get('page', 1)
        limit = params.get('limit', 10)
        offset = (page - 1) * limit
        query += " LIMIT %s OFFSET %s"
        query_params.extend([limit, offset])

        cursor.execute(query, query_params)
        results = cursor.fetchall()
        
        # Parse the concatenated strings into proper data structures
        parsed_results = []
        for row in results:
            organization = dict(row)
            
            # Parse categories
            if organization['categories']:
                organization['categories'] = [
                    {'id': cat.split(':')[0], 'name': cat.split(':')[1]}
                    for cat in organization['categories'].split(',')
                ]
            else:
                organization['categories'] = []

            # Parse locations
            if organization['locations']:
                organization['locations'] = [
                    {
                        'id': loc.split(':')[0],
                        'location_type': loc.split(':')[1],
                        'type': loc.split(':')[2],
                        'address_line1': loc.split(':')[3],
                        'address_line2': loc.split(':')[4],
                        'city': loc.split(':')[5],
                        'state': loc.split(':')[6],
                        'zip_code': loc.split(':')[7],
                        'country': loc.split(':')[8],
                        'is_primary': loc.split(':')[9] == '1'
                    }
                    for loc in organization['locations'].split(',')
                ]
            else:
                organization['locations'] = []

        return parsed_results

    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()





