import uuid
from backend.utilities.errors import ValidationError

def validate_uuid(uuid_string: str) -> None:
    """
    Validate if a string is a valid UUID.
    
    Args:
        uuid_string: The string to validate
        
    Raises:
        ValidationError: If the string is not a valid UUID
    """
    try:
        uuid.UUID(uuid_string)
    except ValueError:
        raise ValidationError(f"Invalid UUID format: {uuid_string}")