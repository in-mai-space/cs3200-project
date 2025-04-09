from typing import Dict, List, Any
from backend.database import db
from backend.utilities.errors import DatabaseError, NotFoundError
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

def get_program_stats(program_id: str) -> Dict[str, Any] | None:
    cursor = db.get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                program_id,
                AVG(effectiveness) AS avg_effectiveness,
                AVG(simplicity) AS avg_simplicity,
                AVG(recommendation) AS avg_recommendation,
                AVG(experience) AS avg_experience,
                COUNT(*) AS total_feedback
            FROM feedback_forms 
            WHERE program_id = %s
            GROUP BY program_id
        """, (program_id,))
        result = cursor.fetchone()
        if not result or result['total_feedback'] == 0:
            return None
        return result
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()
        
def get_program_trends(page: int, limit: int) -> List[Dict[str, Any]]:
    cursor = db.get_db().cursor(dictionary=True)
    try:
        offset = (page - 1) * limit
        cursor.execute('''
            SELECT 
                p.id AS program_id, 
                p.name AS program_name, 
                c.name AS category_name, 
                DATE_FORMAT(a.applied_at, '%Y-%m') AS application_month, 
                COUNT(a.id) AS application_count, 
                SUM(CASE WHEN a.status = 'approved' THEN 1 ELSE 0 END) AS approved_count, 
                SUM(CASE WHEN a.status = 'rejected' THEN 1 ELSE 0 END) AS rejected_count 
            FROM programs p 
            INNER JOIN applications a ON p.id = a.program_id 
            INNER JOIN program_categories pc ON p.id = pc.program_id 
            INNER JOIN categories c ON pc.category_id = c.id 
            WHERE a.applied_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 24 MONTH) 
            GROUP BY p.id, p.name, c.name, DATE_FORMAT(a.applied_at, '%Y-%m') 
            ORDER BY p.name, application_month
            LIMIT %s OFFSET %s
        ''', (limit, offset))
        return cursor.fetchall()
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()
        
    
def get_program_retention(page: int, limit: int) -> List[Dict[str, Any]]:
    cursor = db.get_db().cursor(dictionary=True)
    try:
        offset = (page - 1) * limit
        cursor.execute('''
            SELECT 
                CASE WHEN app_count.application_count > 1 
                    THEN 'Returned users' 
                    ELSE 'One-time users' 
                END AS user_type, 
                AVG(f.effectiveness) AS avg_effectiveness_rating, 
                AVG(f.experience) AS avg_experience_rating, 
                AVG(f.simplicity) AS avg_simplicity_rating, 
                AVG(f.recommendation) AS avg_recommendation_rating, 
                COUNT(DISTINCT f.user_id) AS user_count 
            FROM feedback_forms f 
            INNER JOIN (
                SELECT user_id, COUNT(id) AS application_count 
                FROM applications 
                GROUP BY user_id 
            ) app_count ON f.user_id = app_count.user_id 
            GROUP BY user_type
            LIMIT %s OFFSET %s
        ''', (limit, offset))
        return cursor.fetchall()
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def search_program(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    cursor = db.get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT DISTINCT p.*, o.name as organization_name
            FROM programs p
            JOIN organizations o ON p.organization_id = o.id
            LEFT JOIN program_categories pc ON p.id = pc.program_id
            LEFT JOIN categories c ON pc.category_id = c.id
            LEFT JOIN program_locations pl ON p.id = pl.program_id
            LEFT JOIN locations l ON pl.location_id = l.id
            LEFT JOIN qualifications q ON p.id = q.program_id
            WHERE 1=1
        """
        query_params = []

        # Search text in name, description, or organization name
        if 'search_query' in params and params['search_query']:
            query += " AND (p.name LIKE %s OR p.description LIKE %s OR o.name LIKE %s)"
            search_term = f"%{params['search_query']}%"
            query_params.extend([search_term, search_term, search_term])

        # Filter by category
        if 'category_ids' in params and params['category_ids']:
            query += " AND c.id IN (%s)" % ','.join(['%s'] * len(params['category_ids']))
            query_params.extend(params['category_ids'])

        # Filter by date range
        if 'start_date' in params and params['start_date']:
            query += " AND p.start_date >= %s"
            query_params.append(params['start_date'])
        if 'end_date' in params and params['end_date']:
            query += " AND p.end_date <= %s"
            query_params.append(params['end_date'])

        # Filter by location
        if 'city' in params and params['city']:
            query += " AND l.city = %s"
            query_params.append(params['city'])
        if 'state' in params and params['state']:
            query += " AND l.state = %s"
            query_params.append(params['state'])
        if 'zip_code' in params and params['zip_code']:
            query += " AND l.zip_code = %s"
            query_params.append(params['zip_code'])

        # Apply qualification checks only if user_id is provided
        user_profile = params.get('user_profile', {})
        is_qualified = params.get('is_qualified', None)

        if 'user_id' in params:  # only apply qualifications if user_id is present
            if is_qualified is not None:
                if is_qualified:  # true, the user must meet all qualifications
                    query += """
                        AND NOT EXISTS (
                            SELECT 1 FROM qualifications q
                            WHERE q.program_id = p.id
                            AND NOT (
                                (q.qualification_type = 'income' AND %s BETWEEN q.min_value AND q.max_value) OR
                                (q.qualification_type = 'age' AND TIMESTAMPDIFF(YEAR, %s, CURDATE()) BETWEEN q.min_value AND q.max_value) OR
                                (q.qualification_type = 'family_size' AND %s BETWEEN q.min_value AND q.max_value) OR
                                (q.qualification_type = 'location' AND l.city = q.text_value) OR
                                (q.qualification_type = 'education' AND %s = q.text_value) OR
                                (q.qualification_type = 'disability' AND %s = q.boolean_value) OR
                                (q.qualification_type = 'veteran_status' AND %s = q.boolean_value)
                            )
                        )
                    """
                    # Add user profile values for each qualification
                    query_params.extend([
                        user_profile.get('income'),
                        user_profile.get('date_of_birth'),
                        user_profile.get('family_size'),
                        user_profile.get('location'),
                        user_profile.get('education_level'),
                        user_profile.get('disability_status'),
                        user_profile.get('veteran_status')
                    ])

        # add sorting
        sort_field = params.get('sort_by', 'created_at')
        sort_order = params.get('sort_order', 'DESC')
        query += f" ORDER BY p.{sort_field} {sort_order}"

        # add pagination
        page = params.get('page', 1)
        limit = params.get('limit', 10)
        offset = (page - 1) * limit
        query += " LIMIT %s OFFSET %s"
        query_params.extend([limit, offset])

        cursor.execute(query, query_params)
        return cursor.fetchall()
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()
