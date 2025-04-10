from typing import Dict, List, Any
from backend.database import db
from backend.utilities.errors import DatabaseError, NotFoundError
from mysql.connector import Error as MySQLError

def retrieve_program(program_id: str) -> Dict[str, Any]:
    cursor = db.get_db().cursor()
    try:
        cursor.execute('''
            SELECT 
                p.*,
                o.name as organization_name,
                GROUP_CONCAT(DISTINCT CONCAT(c.id, ':', c.name)) as categories,
                GROUP_CONCAT(DISTINCT CONCAT(l.id, ':', l.location_type, ':', l.type, ':', l.address_line1, ':', l.address_line2, ':', l.city, ':', l.state, ':', l.zip_code, ':', l.country, ':', l.is_primary)) as locations,
                GROUP_CONCAT(DISTINCT CONCAT(q.name, ':', q.description, ':', q.qualification_type, ':', q.min_value, ':', q.max_value, ':', q.text_value, ':', q.boolean_value)) as qualifications
            FROM programs p
            JOIN organizations o ON p.organization_id = o.id
            LEFT JOIN program_categories pc ON p.id = pc.program_id
            LEFT JOIN categories c ON pc.category_id = c.id
            LEFT JOIN locations l ON p.id = l.entity_id AND l.location_type = 'program'
            LEFT JOIN qualifications q ON p.id = q.program_id
            WHERE p.id = %s
            GROUP BY p.id
        ''', (program_id,))
        
        program = cursor.fetchone()
        
        if not program:
            raise NotFoundError(f"Program with id {program_id} not found")

        # Parse the concatenated strings into proper data structures
        if program['categories']:
            program['categories'] = [
                {'id': cat.split(':')[0], 'name': cat.split(':')[1]}
                for cat in program['categories'].split(',')
            ]
        else:
            program['categories'] = []

        if program['locations']:
            program['locations'] = [
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
                for loc in program['locations'].split(',')
            ]
        else:
            program['locations'] = []

        if program['qualifications']:
            program['qualifications'] = [
                {
                    'name': qual.split(':')[0],
                    'description': qual.split(':')[1],
                    'qualification_type': qual.split(':')[2],
                    'min_value': qual.split(':')[3],
                    'max_value': qual.split(':')[4],
                    'text_value': qual.split(':')[5],
                    'boolean_value': qual.split(':')[6] == '1'
                }
                for qual in program['qualifications'].split(',')
            ]
        else:
            program['qualifications'] = []

        return program

    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def update_program_info(program_id: str, data: Dict[str, Any]) -> None:
    cursor = db.get_db().cursor()
    try:
        cursor.execute("START TRANSACTION")

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

        db.get_db().commit()
        return None

    except MySQLError as e:
        db.get_db().rollback()
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def upsert_locations(program_id: str, data: Dict[str, Any]) -> None:
    cursor = db.get_db().cursor()
    try:
        cursor.execute("START TRANSACTION")
        
        cursor.execute('DELETE FROM locations WHERE entity_id = %s AND location_type = %s', (program_id, 'program'))
        
        if 'locations' in data and data['locations']:
            location_values = [
                (
                    'program',
                    program_id,
                    location['type'],
                    location.get('address_line1'),
                    location.get('address_line2'),
                    location['city'],
                    location['state'],
                    location['zip_code'],
                    location.get('country', 'United States'),
                    location.get('is_primary', True)
                )
                for location in data['locations']
            ]
            cursor.executemany('''
                INSERT INTO locations 
                (location_type, entity_id, type, address_line1, address_line2, city, state, zip_code, country, is_primary)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', location_values)
        
        db.get_db().commit()
        return None
    except MySQLError as e:
        db.get_db().rollback()
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def upsert_qualifications(program_id: str, data: Dict[str, Any]) -> None:   
    cursor = db.get_db().cursor()
    try:
        cursor.execute("START TRANSACTION")
        cursor.execute('DELETE FROM qualifications WHERE program_id = %s', (program_id,))
        if 'qualifications' in data and data['qualifications']:
            qualification_values = [
                (
                    program_id,
                    qual['name'],
                    qual['description'],
                    qual['qualification_type'],
                    qual.get('min_value'),
                    qual.get('max_value'),
                    qual.get('text_value'),
                    qual.get('boolean_value')
                )
                for qual in data['qualifications']
            ]
            cursor.executemany('''
                INSERT INTO qualifications 
                (program_id, name, description, qualification_type, min_value, max_value, text_value, boolean_value)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', qualification_values)
        
        db.get_db().commit()
        return None
    except MySQLError as e:
        db.get_db().rollback()
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def upsert_categories(program_id: str, data: Dict[str, Any]) -> None:
    cursor = db.get_db().cursor()
    try:
        cursor.execute("START TRANSACTION")
        cursor.execute('DELETE FROM program_categories WHERE program_id = %s', (program_id,))
        if 'category_ids' in data and data['category_ids']:
            category_values = [(program_id, category_id) for category_id in data['category_ids']]
            cursor.executemany(
                'INSERT INTO program_categories (program_id, category_id) VALUES (%s, %s)',
                category_values
            )
        db.get_db().commit()
        return None
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
    cursor = db.get_db().cursor()
    try:
        offset = (page - 1) * limit
        cursor.execute('''
            SELECT f.*
            FROM feedback_forms f
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
    cursor = db.get_db().cursor()
    try:
        offset = (page - 1) * limit
        cursor.execute('''
            SELECT u.*
            FROM user_profiles u
            INNER JOIN applications a ON u.user_id = a.user_id
            INNER JOIN programs pr ON a.program_id = pr.id
            WHERE pr.id = %s
            LIMIT %s OFFSET %s
        ''', (program_id, limit, offset))
        return cursor.fetchall()
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()
        
def get_program_applications(program_id: str, page: int, limit: int) -> List[Dict[str, Any]]:
    cursor = db.get_db().cursor()
    try:
        offset = (page - 1) * limit
        cursor.execute('''
            SELECT a.*
            FROM applications a
            INNER JOIN programs p ON a.program_id = p.id
            WHERE p.id = %s
            ORDER BY a.applied_at DESC
            LIMIT %s OFFSET %s
        ''', (program_id, limit, offset))
        return cursor.fetchall()
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def get_program_stats(program_id: str) -> Dict[str, Any] | None:
    cursor = db.get_db().cursor()
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
    cursor = db.get_db().cursor()
    try:
        offset = (page - 1) * limit
        cursor.execute('''
            SELECT 
                p.id AS program_id, 
                p.name AS program_name, 
                c.name AS category_name, 
                DATE_FORMAT(a.applied_at, '%%Y-%%m') AS application_month, 
                COUNT(a.id) AS application_count, 
                SUM(CASE WHEN a.status = 'approved' THEN 1 ELSE 0 END) AS approved_count, 
                SUM(CASE WHEN a.status = 'rejected' THEN 1 ELSE 0 END) AS rejected_count 
            FROM programs p 
            INNER JOIN applications a ON p.id = a.program_id 
            INNER JOIN program_categories pc ON p.id = pc.program_id 
            INNER JOIN categories c ON pc.category_id = c.id 
            WHERE a.applied_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 24 MONTH) 
            GROUP BY p.id, p.name, c.name, DATE_FORMAT(a.applied_at, '%%Y-%%m') 
            ORDER BY p.name, application_month
            LIMIT %s OFFSET %s
        ''', (limit, offset))
        return cursor.fetchall()
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()
        
def get_program_retention(page: int, limit: int) -> List[Dict[str, Any]]:
    cursor = db.get_db().cursor()
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
    cursor = db.get_db().cursor()
    try:
        query = """
            SELECT DISTINCT p.*, o.name as organization_name
            FROM programs p
            JOIN organizations o ON p.organization_id = o.id
            LEFT JOIN program_categories pc ON p.id = pc.program_id
            LEFT JOIN categories c ON pc.category_id = c.id
            LEFT JOIN locations l ON p.id = l.entity_id AND l.location_type = 'program'
            LEFT JOIN qualifications q ON p.id = q.program_id
            WHERE 1=1
        """
        query_params = []

        if 'search_query' in params and params['search_query']:
            query += " AND (p.name LIKE %s OR p.description LIKE %s OR o.name LIKE %s)"
            search_term = f"%{params['search_query']}%"
            query_params.extend([search_term, search_term, search_term])

        if 'category_ids' in params and params['category_ids']:
            query += " AND c.id IN (%s)" % ','.join(['%s'] * len(params['category_ids']))
            query_params.extend(params['category_ids'])

        if 'start_date' in params and params['start_date']:
            query += " AND p.start_date >= %s"
            query_params.append(params['start_date'])
        if 'end_date' in params and params['end_date']:
            query += " AND p.end_date <= %s"
            query_params.append(params['end_date'])

        if 'city' in params and params['city']:
            query += " AND l.city = %s"
            query_params.append(params['city'])
        if 'state' in params and params['state']:
            query += " AND l.state = %s"
            query_params.append(params['state'])
        if 'zip_code' in params and params['zip_code']:
            query += " AND l.zip_code = %s"
            query_params.append(params['zip_code'])

        user_profile = params.get('user_profile', {})
        is_qualified = params.get('is_qualified', None)

        if 'user_id' in params:
            if is_qualified is not None:
                if is_qualified:
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
        columns = [desc[0] for desc in cursor.description]
        results = []
        
        for row in cursor.fetchall():
            result = dict(zip(columns, row))
            results.append(result)
            
        return results

    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()
