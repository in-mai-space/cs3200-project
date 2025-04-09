from typing import Dict, Any, List, Optional
from backend.programs.transactions import retrieve_program
from backend.database import db
from backend.utilities.errors import DatabaseError
from mysql.connector import Error as MySQLError

def insert_program(organization_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    cursor = db.get_db().cursor()
    try:
        cursor.execute("START TRANSACTION")
        # insert program
        cursor.execute(
            'INSERT INTO programs (name, description, status, start_date, deadline, end_date, organization_id) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (data['name'], data['description'], data['status'], data['start_date'], data['deadline'], data.get('end_date'), organization_id)
        )
        program_id = cursor.lastrowid

        # bulk insert program-category relationships
        if data['category_ids']:
            category_values = [(program_id, category_id) for category_id in data['category_ids']]
            cursor.executemany(
                'INSERT INTO program_categories (program_id, category_id) VALUES (%s, %s)',
                category_values
            )

        # bulk insert locations and program-location relationships
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

            # get all location IDs that were just inserted
            cursor.execute('SELECT LAST_INSERT_ID()')
            first_location_id = cursor.fetchone()[0]
            location_ids = range(first_location_id, first_location_id + len(data['locations']))
            
            # bulk insert program-location relationships
            program_location_values = [(program_id, loc_id) for loc_id in location_ids]
            cursor.executemany(
                'INSERT INTO program_locations (program_id, location_id) VALUES (%s, %s)',
                program_location_values
            )

        # bulk insert qualifications
        if 'qualifications' in data and data['qualifications']:
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