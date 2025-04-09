from typing import Dict, List, Any
from backend.database import db
from backend.utilities.errors import DatabaseError, ConflictError, NotFoundError
from mysql.connector import Error as MySQLError

def retrieve_program(program_id: str) -> Dict[str, Any]:
    cursor = db.get_db().cursor(dictionary=True)
    try:
        # get program details
        cursor.execute('''
            SELECT p.*, o.name as organization_name
            FROM programs p
            JOIN organizations o ON p.organization_id = o.id
            WHERE p.id = %s
        ''', (program_id,))
        program = cursor.fetchone()
        
        if not program:
            raise NotFoundError(f"Program with id {program_id} not found")

        # get categories
        cursor.execute('''
            SELECT c.id, c.name
            FROM program_categories pc
            JOIN categories c ON pc.category_id = c.id
            WHERE pc.program_id = %s
        ''', (program_id,))
        categories = cursor.fetchall()
        program['category_ids'] = [cat['id'] for cat in categories]
        program['categories'] = categories

        # get locations
        cursor.execute('''
            SELECT l.*
            FROM program_locations pl
            JOIN locations l ON pl.location_id = l.id
            WHERE pl.program_id = %s
        ''', (program_id,))
        program['locations'] = cursor.fetchall()

        # get qualifications
        cursor.execute('''
            SELECT *
            FROM qualifications
            WHERE program_id = %s
        ''', (program_id,))
        program['qualifications'] = cursor.fetchall()

        return program

    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def update_program_info(program_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    cursor = db.get_db().cursor()
    try:
        cursor.execute("START TRANSACTION")

        # update program details
        update_fields = []
        update_values = []
        
        for field in ['name', 'description', 'status', 'start_date', 'deadline', 'end_date']:
            if field in data:
                update_fields.append(f"{field} = %s")
                update_values.append(data[field])
        
        if update_fields:
            update_values.append(program_id)
            cursor.execute(
                f'UPDATE programs SET {", ".join(update_fields)} WHERE id = %s',
                update_values
            )

        # handle categories
        if 'category_ids' in data:
            # delete existing categories
            cursor.execute('DELETE FROM program_categories WHERE program_id = %s', (program_id,))
            
            # insert new categories
            if data['category_ids']:
                category_values = [(program_id, category_id) for category_id in data['category_ids']]
                cursor.executemany(
                    'INSERT INTO program_categories (program_id, category_id) VALUES (%s, %s)',
                    category_values
                )

        # handle locations
        if 'locations' in data:
            # get existing location IDs
            cursor.execute('SELECT location_id FROM program_locations WHERE program_id = %s', (program_id,))
            existing_location_ids = [row[0] for row in cursor.fetchall()]
            
            # delete existing locations and relationships
            if existing_location_ids:
                cursor.execute('DELETE FROM locations WHERE id IN (%s)' % ','.join(['%s'] * len(existing_location_ids)), existing_location_ids)
                cursor.execute('DELETE FROM program_locations WHERE program_id = %s', (program_id,))
            
            # insert new locations and relationships
            if data['locations']:
                location_values = [
                    ('program', program_id, loc['type'], loc.get('address_line1'), loc.get('address_line2'),
                     loc['city'], loc['state'], loc['zip_code'], loc.get('country', 'United States'),
                     loc.get('is_primary', True))
                    for loc in data['locations']
                ]
                cursor.executemany(
                    'INSERT INTO locations (location_type, entity_id, type, address_line1, address_line2, city, state, zip_code, country, is_primary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    location_values
                )

                cursor.execute('SELECT LAST_INSERT_ID()')
                first_location_id = cursor.fetchone()[0]
                location_ids = range(first_location_id, first_location_id + len(data['locations']))
                
                program_location_values = [(program_id, loc_id) for loc_id in location_ids]
                cursor.executemany(
                    'INSERT INTO program_locations (program_id, location_id) VALUES (%s, %s)',
                    program_location_values
                )

        # handle qualifications
        if 'qualifications' in data:
            # delete existing qualifications
            cursor.execute('DELETE FROM qualifications WHERE program_id = %s', (program_id,))
            
            # insert new qualifications
            if data['qualifications']:
                qualification_values = [
                    (program_id, qual['name'], qual['description'], qual['qualification_type'],
                     qual.get('min_value'), qual.get('max_value'), qual.get('text_value'),
                     qual.get('boolean_value'))
                    for qual in data['qualifications']
                ]
                cursor.executemany(
                    'INSERT INTO qualifications (program_id, name, description, qualification_type, min_value, max_value, text_value, boolean_value) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                    qualification_values
                )

        db.get_db().commit()
        return retrieve_program(program_id)

    except MySQLError as e:
        db.get_db().rollback()
        raise DatabaseError(str(e))
    finally:
        cursor.close()


def remove_program(program_id: str) -> None:
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM programs WHERE id = %s', (program_id,))
        db.get_db().commit()
    except MySQLError as e:
        db.get_db().rollback()
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def get_program_feedback(program_id: str, page: int, limit: int) -> List[Dict[str, Any]]:
    cursor = db.get_db().cursor(dictionary=True)
    try:
        offset = (page - 1) * limit
        cursor.execute('''
            SELECT f.*
            FROM feedbacks f
            INNER JOIN programs p ON f.program_id = p.id
            WHERE p.id = %s
            ORDER BY f.created_at DESC
            LIMIT %s OFFSET %s
        ''', (program_id, limit, offset))
        return cursor.fetchall()
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def get_program_profiles(program_id: str, page: int, limit: int) -> List[Dict[str, Any]]:
    cursor = db.get_db().cursor(dictionary=True)
    try:
        offset = (page - 1) * limit
        cursor.execute('''
            SELECT p.*
            FROM profiles p
            INNER JOIN applications a ON p.id = a.profile_id
            INNER JOIN programs pr ON a.program_id = pr.id
            WHERE pr.id = %s
            ORDER BY a.created_at DESC
            LIMIT %s OFFSET %s
        ''', (program_id, limit, offset))
        return cursor.fetchall()
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()
        
def get_program_applications(program_id: str, page: int, limit: int) -> List[Dict[str, Any]]:
    cursor = db.get_db().cursor(dictionary=True)
    try:
        offset = (page - 1) * limit
        cursor.execute('''
            SELECT a.*
            FROM applications a
            INNER JOIN programs p ON a.program_id = p.id
            WHERE p.id = %s
            ORDER BY a.created_at DESC
            LIMIT %s OFFSET %s
        ''', (program_id, limit, offset))
        return cursor.fetchall()
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()