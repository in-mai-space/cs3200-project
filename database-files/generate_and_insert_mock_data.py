from faker import Faker
import uuid
import random
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

fake = Faker()

# Constants
NUM_USERS = 100
NUM_ORGANIZATIONS = 20
NUM_PROGRAMS = 50
NUM_CATEGORIES = 10
NUM_APPLICATIONS = 200
NUM_FEEDBACK_FORMS = 150
NUM_LOCATIONS = 100

# Database configuration from environment variables
DB_CONFIG = {
    'host': 'localhost',  # Use localhost since we're connecting from the host machine
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('MYSQL_ROOT_PASSWORD', 'password'),
    'port': 3200,  # Use the mapped port on the host
    'database': os.getenv('DB_NAME', 'uplift')
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def generate_uuid():
    return str(uuid.uuid4())

def generate_date(start_date, end_date):
    return fake.date_between(start_date=start_date, end_date=end_date)

def generate_timestamp(start_date, end_date):
    return fake.date_time_between(start_date=start_date, end_date=end_date)

def insert_users(connection):
    cursor = connection.cursor()
    users = []
    for _ in range(NUM_USERS):
        user = {
            'id': generate_uuid(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'type': random.choice(['admin', 'user', 'data_analyst', 'organization_admin']),
            'registered_at': generate_timestamp('-1y', 'now')
        }
        users.append(user)
    
    insert_query = """
    INSERT INTO users (id, first_name, last_name, type, registered_at)
    VALUES (%(id)s, %(first_name)s, %(last_name)s, %(type)s, %(registered_at)s)
    """
    cursor.executemany(insert_query, users)
    connection.commit()
    cursor.close()
    return users

def insert_user_profiles(connection, users):
    cursor = connection.cursor()
    profiles = []
    for user in users:
        profile = {
            'user_id': user['id'],
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=80),
            'gender': random.choice(['Male', 'Female', 'Other']),
            'income': random.randint(20000, 150000),
            'education_level': random.choice(['High School', 'Bachelors', 'Masters', 'PhD']),
            'employment_status': random.choice(['Employed', 'Unemployed', 'Part-time', 'Self-employed']),
            'veteran_status': random.choice([True, False]),
            'disability_status': random.choice([True, False]),
            'ssn': fake.ssn(),
            'verification_status': random.choice(['unverified', 'pending', 'verified']),
            'verification_date': generate_timestamp('-1y', 'now'),
            'last_updated': generate_timestamp('-1y', 'now')
        }
        profiles.append(profile)
    
    insert_query = """
    INSERT INTO user_profiles 
    (user_id, date_of_birth, gender, income, education_level, employment_status, 
     veteran_status, disability_status, ssn, verification_status, verification_date, last_updated)
    VALUES 
    (%(user_id)s, %(date_of_birth)s, %(gender)s, %(income)s, %(education_level)s, %(employment_status)s,
     %(veteran_status)s, %(disability_status)s, %(ssn)s, %(verification_status)s, %(verification_date)s, %(last_updated)s)
    """
    cursor.executemany(insert_query, profiles)
    connection.commit()
    cursor.close()

def insert_organizations(connection):
    cursor = connection.cursor()
    organizations = []
    for _ in range(NUM_ORGANIZATIONS):
        org = {
            'id': generate_uuid(),
            'name': fake.company(),
            'description': fake.paragraph(nb_sentences=3),
            'website_url': fake.url(),
            'is_verified': random.choice([True, False]),
            'verified_at': generate_timestamp('-1y', 'now') if random.random() > 0.3 else None,
            'created_at': generate_timestamp('-2y', '-1y'),
            'updated_at': generate_timestamp('-1y', 'now')
        }
        organizations.append(org)
    
    insert_query = """
    INSERT INTO organizations 
    (id, name, description, website_url, is_verified, verified_at, created_at, updated_at)
    VALUES 
    (%(id)s, %(name)s, %(description)s, %(website_url)s, %(is_verified)s, %(verified_at)s, %(created_at)s, %(updated_at)s)
    """
    cursor.executemany(insert_query, organizations)
    connection.commit()
    cursor.close()
    return organizations

def insert_categories(connection):
    cursor = connection.cursor()
    
    # First, get existing categories
    cursor.execute("SELECT name FROM categories")
    existing_categories = {row[0] for row in cursor.fetchall()}
    
    # Define all possible categories
    all_categories = [
        'Financial Assistance',
        'Education',
        'Housing',
        'Healthcare',
        'Employment',
        'Veterans',
        'Food Assistance',
        'Child Care',
        'Transportation',
        'Legal Services'
    ]
    
    # Only insert categories that don't exist
    new_categories = [name for name in all_categories if name not in existing_categories]
    category_data = [{'id': generate_uuid(), 'name': name} for name in new_categories]
    
    if category_data:
        insert_query = """
        INSERT INTO categories (id, name)
        VALUES (%(id)s, %(name)s)
        """
        cursor.executemany(insert_query, category_data)
        connection.commit()
        print(f"Inserted {len(category_data)} new categories")
    else:
        print("All categories already exist in the database")
    
    # Get all categories (existing and newly inserted) for reference
    cursor.execute("SELECT id, name FROM categories")
    categories = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]
    
    cursor.close()
    return categories

def insert_programs(connection, organizations):
    cursor = connection.cursor()
    programs = []
    for _ in range(NUM_PROGRAMS):
        org = random.choice(organizations)
        start_date = generate_date('-1y', '+1y')
        program = {
            'id': generate_uuid(),
            'name': fake.sentence(nb_words=4),
            'description': fake.paragraph(nb_sentences=3),
            'status': random.choice(['open', 'close']),
            'start_date': start_date,
            'deadline': generate_timestamp(start_date, start_date + timedelta(days=180)),
            'end_date': generate_date(start_date + timedelta(days=30), start_date + timedelta(days=365)),
            'organization_id': org['id'],
            'created_at': generate_timestamp('-2y', '-1y'),
            'updated_at': generate_timestamp('-1y', 'now')
        }
        programs.append(program)
    
    insert_query = """
    INSERT INTO programs 
    (id, name, description, status, start_date, deadline, end_date, organization_id, created_at, updated_at)
    VALUES 
    (%(id)s, %(name)s, %(description)s, %(status)s, %(start_date)s, %(deadline)s, %(end_date)s, 
     %(organization_id)s, %(created_at)s, %(updated_at)s)
    """
    cursor.executemany(insert_query, programs)
    connection.commit()
    cursor.close()
    return programs

def insert_qualifications(connection, programs):
    cursor = connection.cursor()
    qualifications = []
    qualification_types = [
        'income', 'age', 'family_size', 'location', 'education',
        'disability', 'veteran_status', 'citizenship', 'other'
    ]
    
    for program in programs:
        num_qualifications = random.randint(1, 4)
        for _ in range(num_qualifications):
            qual_type = random.choice(qualification_types)
            qual = {
                'program_id': program['id'],
                'name': fake.sentence(nb_words=3),
                'description': fake.sentence(),
                'qualification_type': qual_type,
                'min_value': random.uniform(0, 100000) if qual_type in ['income', 'age'] else None,
                'max_value': random.uniform(100000, 200000) if qual_type in ['income', 'age'] else None,
                'text_value': fake.city() if qual_type == 'location' else None,
                'boolean_value': random.choice([True, False]) if qual_type in ['disability', 'veteran_status'] else None
            }
            qualifications.append(qual)
    
    insert_query = """
    INSERT INTO qualifications 
    (program_id, name, description, qualification_type, min_value, max_value, text_value, boolean_value)
    VALUES 
    (%(program_id)s, %(name)s, %(description)s, %(qualification_type)s, %(min_value)s, %(max_value)s, 
     %(text_value)s, %(boolean_value)s)
    """
    cursor.executemany(insert_query, qualifications)
    connection.commit()
    cursor.close()

def insert_applications(connection, users, programs):
    cursor = connection.cursor()
    
    # First, get existing user-program combinations
    cursor.execute("SELECT user_id, program_id FROM applications")
    existing_combinations = {(row[0], row[1]) for row in cursor.fetchall()}
    
    applications = []
    for _ in range(NUM_APPLICATIONS):
        user = random.choice(users)
        program = random.choice(programs)
        
        # Skip if this user-program combination already exists
        if (user['id'], program['id']) in existing_combinations:
            continue
            
        applied_at = generate_timestamp('-1y', 'now')
        app = {
            'id': generate_uuid(),
            'user_id': user['id'],
            'program_id': program['id'],
            'status': random.choice([
                'draft', 'submitted', 'under_review', 'additional_info_needed',
                'approved', 'rejected', 'waitlisted', 'withdrawn'
            ]),
            'qualification_status': random.choice(['pending', 'verified', 'incomplete', 'rejected']),
            'applied_at': applied_at,
            'decision_date': generate_timestamp(applied_at, 'now') if random.random() > 0.3 else None,
            'decision_notes': fake.paragraph(nb_sentences=2) if random.random() > 0.5 else None,
            'last_updated': generate_timestamp(applied_at, 'now')
        }
        applications.append(app)
        # Add to existing combinations to prevent duplicates in this batch
        existing_combinations.add((user['id'], program['id']))
    
    if applications:
        insert_query = """
        INSERT INTO applications 
        (id, user_id, program_id, status, qualification_status, applied_at, decision_date, decision_notes, last_updated)
        VALUES 
        (%(id)s, %(user_id)s, %(program_id)s, %(status)s, %(qualification_status)s, %(applied_at)s, 
         %(decision_date)s, %(decision_notes)s, %(last_updated)s)
        """
        cursor.executemany(insert_query, applications)
        connection.commit()
        print(f"Inserted {len(applications)} new applications")
    else:
        print("No new applications to insert (all possible combinations already exist)")
    
    cursor.close()

def insert_feedback_forms(connection, programs, users):
    cursor = connection.cursor()
    
    # First, get existing user-program feedback combinations
    cursor.execute("SELECT user_id, program_id FROM feedback_forms")
    existing_combinations = {(row[0], row[1]) for row in cursor.fetchall()}
    
    feedback_forms = []
    for _ in range(NUM_FEEDBACK_FORMS):
        program = random.choice(programs)
        user = random.choice(users)
        
        # Skip if this user-program combination already has feedback
        if (user['id'], program['id']) in existing_combinations:
            continue
            
        feedback = {
            'id': generate_uuid(),
            'program_id': program['id'],
            'user_id': user['id'],
            'title': fake.sentence(nb_words=4),
            'created_at': generate_timestamp('-1y', 'now'),
            'updated_at': generate_timestamp('-1y', 'now'),
            'effectiveness': random.randint(1, 5),
            'experience': random.randint(1, 5),
            'simplicity': random.randint(1, 5),
            'recommendation': random.randint(1, 5),
            'improvement': fake.paragraph(nb_sentences=3)
        }
        feedback_forms.append(feedback)
        # Add to existing combinations to prevent duplicates in this batch
        existing_combinations.add((user['id'], program['id']))
    
    if feedback_forms:
        insert_query = """
        INSERT INTO feedback_forms 
        (id, program_id, user_id, title, created_at, updated_at, effectiveness, experience, 
         simplicity, recommendation, improvement)
        VALUES 
        (%(id)s, %(program_id)s, %(user_id)s, %(title)s, %(created_at)s, %(updated_at)s, 
         %(effectiveness)s, %(experience)s, %(simplicity)s, %(recommendation)s, %(improvement)s)
        """
        cursor.executemany(insert_query, feedback_forms)
        connection.commit()
        print(f"Inserted {len(feedback_forms)} new feedback forms")
    else:
        print("No new feedback forms to insert (all possible combinations already exist)")
    
    cursor.close()

def insert_locations(connection, organizations, programs, users):
    cursor = connection.cursor()
    locations = []
    
    # Generate organization locations
    for org in organizations:
        num_locations = random.randint(1, 3)
        for i in range(num_locations):
            loc = {
                'id': generate_uuid(),
                'location_type': 'organization',
                'entity_id': org['id'],
                'type': random.choice(['virtual', 'physical']),
                'address_line1': fake.street_address() if random.random() > 0.2 else None,
                'address_line2': fake.secondary_address() if random.random() > 0.5 else None,
                'city': fake.city(),
                'state': fake.state(),
                'zip_code': fake.zipcode(),
                'country': 'United States',
                'is_primary': i == 0,
                'created_at': generate_timestamp('-2y', '-1y'),
                'updated_at': generate_timestamp('-1y', 'now')
            }
            locations.append(loc)
    
    # Generate program locations
    for program in programs:
        if random.random() > 0.3:  # 70% chance of having a location
            loc = {
                'id': generate_uuid(),
                'location_type': 'program',
                'entity_id': program['id'],
                'type': random.choice(['virtual', 'physical']),
                'address_line1': fake.street_address() if random.random() > 0.2 else None,
                'address_line2': fake.secondary_address() if random.random() > 0.5 else None,
                'city': fake.city(),
                'state': fake.state(),
                'zip_code': fake.zipcode(),
                'country': 'United States',
                'is_primary': True,
                'created_at': generate_timestamp('-2y', '-1y'),
                'updated_at': generate_timestamp('-1y', 'now')
            }
            locations.append(loc)
    
    # Generate user locations
    for user in users:
        if random.random() > 0.2:  # 80% chance of having a location
            loc = {
                'id': generate_uuid(),
                'location_type': 'user',
                'entity_id': user['id'],
                'type': 'physical',
                'address_line1': fake.street_address(),
                'address_line2': fake.secondary_address() if random.random() > 0.5 else None,
                'city': fake.city(),
                'state': fake.state(),
                'zip_code': fake.zipcode(),
                'country': 'United States',
                'is_primary': True,
                'created_at': generate_timestamp('-2y', '-1y'),
                'updated_at': generate_timestamp('-1y', 'now')
            }
            locations.append(loc)
    
    insert_query = """
    INSERT INTO locations 
    (id, location_type, entity_id, type, address_line1, address_line2, city, state, 
     zip_code, country, is_primary, created_at, updated_at)
    VALUES 
    (%(id)s, %(location_type)s, %(entity_id)s, %(type)s, %(address_line1)s, %(address_line2)s, 
     %(city)s, %(state)s, %(zip_code)s, %(country)s, %(is_primary)s, %(created_at)s, %(updated_at)s)
    """
    cursor.executemany(insert_query, locations)
    connection.commit()
    cursor.close()
    return locations

def insert_user_programs(connection, users, programs):
    cursor = connection.cursor()
    user_programs = []
    for user in users:
        num_programs = random.randint(0, 5)
        selected_programs = random.sample(programs, min(num_programs, len(programs)))
        for program in selected_programs:
            user_programs.append({
                'user_id': user['id'],
                'program_id': program['id']
            })
    
    insert_query = """
    INSERT INTO user_programs (user_id, program_id)
    VALUES (%(user_id)s, %(program_id)s)
    """
    cursor.executemany(insert_query, user_programs)
    connection.commit()
    cursor.close()

def insert_organization_categories(connection, organizations, categories):
    cursor = connection.cursor()
    org_categories = []
    for org in organizations:
        num_categories = random.randint(1, 4)
        selected_categories = random.sample(categories, min(num_categories, len(categories)))
        for category in selected_categories:
            org_categories.append({
                'organization_id': org['id'],
                'category_id': category['id']
            })
    
    insert_query = """
    INSERT INTO organization_categories (organization_id, category_id)
    VALUES (%(organization_id)s, %(category_id)s)
    """
    cursor.executemany(insert_query, org_categories)
    connection.commit()
    cursor.close()

def insert_program_categories(connection, programs, categories):
    cursor = connection.cursor()
    program_categories = []
    for program in programs:
        num_categories = random.randint(1, 3)
        selected_categories = random.sample(categories, min(num_categories, len(categories)))
        for category in selected_categories:
            program_categories.append({
                'program_id': program['id'],
                'category_id': category['id']
            })
    
    insert_query = """
    INSERT INTO program_categories (program_id, category_id)
    VALUES (%(program_id)s, %(category_id)s)
    """
    cursor.executemany(insert_query, program_categories)
    connection.commit()
    cursor.close()

def insert_organization_locations(connection, organizations, locations):
    cursor = connection.cursor()
    org_locations = []
    org_locations_dict = {}
    
    # Group locations by organization
    for loc in locations:
        if loc['location_type'] == 'organization':
            if loc['entity_id'] not in org_locations_dict:
                org_locations_dict[loc['entity_id']] = []
            org_locations_dict[loc['entity_id']].append(loc['id'])
    
    # Create relationships
    for org in organizations:
        if org['id'] in org_locations_dict:
            for loc_id in org_locations_dict[org['id']]:
                org_locations.append({
                    'organization_id': org['id'],
                    'location_id': loc_id
                })
    
    insert_query = """
    INSERT INTO organization_locations (organization_id, location_id)
    VALUES (%(organization_id)s, %(location_id)s)
    """
    cursor.executemany(insert_query, org_locations)
    connection.commit()
    cursor.close()

def main():
    try:        
        # Connect to database
        connection = get_db_connection()
        if not connection:
            return
        
        print("Generating and inserting mock data...")
        
        # Insert data in the correct order to maintain referential integrity
        users = insert_users(connection)
        print("Inserted users")
        
        insert_user_profiles(connection, users)
        print("Inserted user profiles")
        
        organizations = insert_organizations(connection)
        print("Inserted organizations")
        
        categories = insert_categories(connection)
        print("Inserted categories")
        
        programs = insert_programs(connection, organizations)
        print("Inserted programs")
        
        insert_qualifications(connection, programs)
        print("Inserted qualifications")
        
        insert_applications(connection, users, programs)
        print("Inserted applications")
        
        insert_feedback_forms(connection, programs, users)
        print("Inserted feedback forms")
        
        locations = insert_locations(connection, organizations, programs, users)
        print("Inserted locations")
        
        insert_user_programs(connection, users, programs)
        print("Inserted user programs")
        
        insert_organization_categories(connection, organizations, categories)
        print("Inserted organization categories")
        
        insert_program_categories(connection, programs, categories)
        print("Inserted program categories")
        
        insert_organization_locations(connection, organizations, locations)
        print("Inserted organization locations")
        
        print("All data has been successfully inserted!")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main() 