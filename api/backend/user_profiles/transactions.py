from typing import Dict, Any, Optional

from pymysql import MySQLError
from backend.database import db
from backend.utilities.errors import DatabaseError, NotFoundError
import pymysql.cursors

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

def get_user_profile_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    cursor = db.get_db().cursor(pymysql.cursors.DictCursor)
    try:
        query = """
            SELECT 
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
                verification_date,
                last_updated
            FROM user_profiles
            WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        profile = cursor.fetchone()
        return profile
    except Exception as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def update_user_profile(user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing user profile record in the database.

    Args:
        user_id (str): The UUID of the user profile to update.
        update_data (Dict[str, Any]): Dictionary containing the fields to update.
            Supported keys are:
              - date_of_birth
              - gender
              - income
              - education_level
              - employment_status
              - veteran_status
              - disability_status
              - ssn
              - verification_status
              - verification_date

    Returns:
        Dict[str, Any]: The updated user profile record.

    Raises:
        NotFoundError: If no user profile exists with the given user_id.
        DatabaseError: If there's an error updating the user profile.
    """
    cursor = db.get_db().cursor()
    try:
        update_fields = []
        values = []
        # Define the allowed fields for the update.
        allowed_fields = [
            'date_of_birth', 'gender', 'income', 'education_level',
            'employment_status', 'veteran_status', 'disability_status',
            'ssn', 'verification_status', 'verification_date'
        ]
        for field in allowed_fields:
            if field in update_data:
                update_fields.append(f"{field} = %s")
                values.append(update_data[field])
        if not update_fields:
            raise DatabaseError("No valid fields to update")
        # Append the user_id for the WHERE clause.
        values.append(user_id)
        query = f"UPDATE user_profiles SET {', '.join(update_fields)} WHERE user_id = %s"
        cursor.execute(query, values)
        db.get_db().commit()
        
        # Fetch the updated user profile record.
        cursor.execute("SELECT * FROM user_profiles WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if not result:
            raise NotFoundError(f"User profile with id {user_id} does not exist")
        return result
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()

def delete_user_profile(user_id: str) -> Dict[str, Any]:
    """
    Delete a user's profile from the database.

    Args:
        user_id (str): The UUID of the user profile to delete.

    Returns:
        Dict[str, Any]: An empty dict or additional info if needed.

    Raises:
        DatabaseError: If there's an error deleting the user profile.
    """
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM user_profiles WHERE user_id = %s', (user_id,))
        db.get_db().commit()
        # Return an empty dict to be consistent with a structure that could return additional details.
        return {}
    except MySQLError as e:
        raise DatabaseError(str(e))
    finally:
        cursor.close()
