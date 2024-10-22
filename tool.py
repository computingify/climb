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
    # Regex pattern to match yyyy/mm/dd or mm/dd/yyyy formats
    pattern = r'(\b\d{4}/\d{2}/\d{2}\b)|(\b\d{2}/\d{2}/\d{4}\b)'

    # Find the birth date using the regex pattern
    match = re.search(pattern, birth_date)
    if not match:
        raise NameError('Invalid birth date format. Expected yyyy/mm/dd or mm/dd/yyyy.')

    # Extract the matched date
    extracted_date = match.group()

    # Determine the date format
    if re.match(r'^\d{4}/\d{2}/\d{2}$', extracted_date):
        date_format = "%Y/%m/%d"
    else:
        date_format = "%m/%d/%Y"

    # Convert the birth date string to a datetime object
    return datetime.strptime(extracted_date, date_format)

def similar(a, b):
    """Return the similarity ratio between two strings."""
    return SequenceMatcher(None, a, b).ratio()