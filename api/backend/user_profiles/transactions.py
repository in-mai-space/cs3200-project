from typing import Dict, List, Any
from backend.database import db
from backend.utilities.errors import DatabaseError, ConflictError, NotFoundError
from mysql.connector import Error as MySQLError

def insert_user_profile(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Insert a new user profile record into the database.

    Args:
        data (Dict[str, Any]): A dictionary containing the user's profile data.
            Required keys:
                - 'user_id': The unique identifier for the user (must match a valid user in the users table).
                - 'ssn': The user's Social Security Number.
            Optional keys:
                - 'date_of_birth': The user's date of birth.
                - 'gender': The user's gender.
                - 'income': The user's income.
                - 'education_level': The user's level of education.
                - 'employment_status': The user's employment status.
                - 'veteran_status': Boolean indicating veteran status (defaults to False if not provided).
                - 'disability_status': Boolean indicating disability status (defaults to False if not provided).
                - 'verification_status': The verification status (defaults to 'unverified' if not provided).
                - 'verification_date': The timestamp when the profile was verified.
    
    Returns:
        Dict[str, Any]: A message confirming the profile creation.
    
    Raises:
        DatabaseError: If an error occurs during the profile creation.
    """
    cursor = db.get_db().cursor()
    try:
        query = """
        INSERT INTO user_profiles (
            user_id,
            date_of_birth,
            gender,
            income,
            education_level,
            employment_status,
            veteran_status,
            disability_status,
            ssn,
            verification_status,
            verification_date
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        cursor.execute(query, (
            data['user_id'],                                   # Required field
            data.get('date_of_birth'),                         # Optional: will be NULL if missing
            data.get('gender'),
            data.get('income'),
            data.get('education_level'),
            data.get('employment_status'),
            data.get('veteran_status', False),                 # Defaults to False
            data.get('disability_status', False),              # Defaults to False
            data['ssn'],                                       # Required field
            data.get('verification_status', 'unverified'),     # Defaults to 'unverified'
            data.get('verification_date')                      # Optional: will be NULL if missing
        ))
        db.get_db().commit()
        return {"message": "User profile created successfully"}
    except Exception as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()
