import re
from difflib import SequenceMatcher
from datetime import datetime

NAME_MAX_SIZE = 16

def format_name(name_raw):
    name = name_raw.capitalize()
    # Check if the name contain only allowed characters
    if not re.match(r'^[a-zA-Z-]+$', name):
        raise NameError('FirstName and LastName must contain only letters and hyphens.')

    # Check if the FirstName and LastName exceed the maximum length
    if len(name) > NAME_MAX_SIZE:
        raise NameError(f'FirstName and LastName must be {NAME_MAX_SIZE} characters or less.')
    
    return name

def checkId(id):
    if not re.match(r'^[1-9]+$', id):
        raise NameError(f'id is not in correct format')

def format_birth_date(birth_date):
    # Validate the birth date format
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', birth_date):
        raise NameError('Invalid birth date format. Expected yyyy-mm-dd.')

    # Convert the birth date string to a datetime object
    return datetime.strptime(birth_date, "%Y-%m-%d")

def similar(a, b):
    """Return the similarity ratio between two strings."""
    return SequenceMatcher(None, a, b).ratio()