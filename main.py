import flask
from flask import request, jsonify
from db import data_base, UserNotFoundError
from datetime import datetime
import re
from email_validator import validate_email, EmailNotValidError
from collections import namedtuple
from difflib import SequenceMatcher

NAME_MAX_SIZE = 16

# Micro REST API creation
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create Data Base object
db = data_base()

# definition de l'ensemble des routes prises en charge par l'API
@app.route('/', methods=['GET'])
def home():
    return flask.render_template('index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return flask.send_from_directory('web_pages/js', path)

@app.route('/styles/<path:path>')
def send_styles(path):
    return flask.send_from_directory('web_pages/styles', path)

@app.route('/api/v1/resources/users/all', methods=['GET'])
def api_get_all_users():
    return jsonify(db.get_all_users())

@app.route('/api/v1/resources/user', methods=['GET'])
def api_get_user():
    query_parameters = request.args

    # Check if the FirstName and LastName contain only allowed characters
    first_name_val = query_parameters.get('FirstName')
    last_name_val = query_parameters.get('LastName')
    id_val = query_parameters.get('Id')
    if (first_name_val is None or last_name_val is None) and id_val is None:
        return jsonify({'error': 'FirstName and LastName are required parameters. Or use Id'}), 400

    try:

        if first_name_val is not None and last_name_val is not None:
            id_val = search_user(first_name_val, last_name_val)
        if id_val is not None:
            _checkId(id_val)
            user = db.is_user_id_exist(id_val)
            
    except NameError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify(user)

@app.route('/api/v1/resources/user', methods=['POST'])
def api_add_user():
    query_parameters = request.args

    # Validate FirstName and LastName format
    first_name_val = request.form.get('FirstName')
    last_name_val = request.form.get('LastName')
    birth_date_str = request.form.get('BirthDate')
    email_val = request.form.get('email')
    print(f"first_name_val = {first_name_val} last_name_val = {last_name_val} birth_date_str = {birth_date_str} email_val = {email_val}")

    if first_name_val is None or last_name_val is None:
        print('FirstName and LastName are required parameters.')
        return jsonify({'error': 'FirstName and LastName are required parameters.'}), 400

    try:
        first_name_val = _format_name(first_name_val)
        last_name_val = _format_name(last_name_val)
    except NameError as e:
        print(f'error {str(e)}')
        return jsonify({'error': str(e)}), 400
    
    # Validate the birth date format (if provided)
    if birth_date_str:
        try:
            birth_date_val = _format_birth_date(birth_date_str)
        except NameError as e:
            print(f'error {str(e)}')
            return jsonify({'error': str(e)}), 400

    # Validate the email address format (if provided)
    if email_val:
        try:
            validate_email(email_val)
        except EmailNotValidError:
            print('Invalid email address format.')
            return jsonify({'error': 'Invalid email address format.'}), 400

    # Store data into DB
    user_data_format = namedtuple('User', ['first_name', 'last_name', 'birth_date', 'email'])
    user_data = user_data_format(first_name=first_name_val, last_name=last_name_val, birth_date=birth_date_val, email=email_val)
    db.create_user(user_data)
    return jsonify("success")

def search_user(first_name, last_name):
    # Get partial first name and last name from the query parameters
    first_name_val = first_name.strip().lower()
    last_name_val = last_name.strip().lower()

    if not first_name_val and not last_name_val:
        return jsonify({'error': 'At least one of FirstName or LastName must be provided.'}), 400

    # Get all users from the database
    all_users = db.get_all_users()

    # Function to find best match given the first and last names
    def find_best_match(first_name, last_name):
        best_match = None
        best_score = 0

        for user in all_users:
            first_name_score = _similar(first_name, user[1].lower()) if first_name else 0
            last_name_score = _similar(last_name, user[2].lower()) if last_name else 0
            score = first_name_score + last_name_score

            if score > best_score:
                best_score = score
                best_match = user

        return best_match

    # First attempt with original order
    best_match = find_best_match(first_name_val, last_name_val)

    if best_match:
        return str(best_match[0])

    # If no match found, try with reversed order
    best_match = find_best_match(last_name_val, first_name_val)

    if best_match:
        return str(best_match[0])
    else:
        raise NameError(f'FirstName: {first_name} and LastName: {last_name} Unknown in DB.')

def _similar(a, b):
    """Return the similarity ratio between two strings."""
    return SequenceMatcher(None, a, b).ratio()

@app.route('/api/v1/resources/session/add_user', methods=['POST'])
def api_add_user_to_session():
    
    # Get the user data from the request
    query_parameters = request.args
    user_id = query_parameters.get('UserId')
    
    # Check if the user_id is provided
    if user_id is None:
        return jsonify({'error': 'UserId parameter is required.'}), 400
    
    try:
        int(user_id)
    except ValueError:
        return jsonify({'error': 'Invalid user Id format, must be an integer.'}), 400

    # Check if the user ID exists in the database
    try:
        db.is_user_id_exist(user_id)
    except UserNotFoundError as e:
        return jsonify({'error': str(e)}), 404

    # Get session ID for the current day
    today = datetime.now().date()
    session_id = db.get_session(today)

    # Assign the user to a session
    db.add_user_to_session(session_id, user_id, datetime.now().strftime("%H:%M"))

    # Return a success message
    return jsonify({'message': 'User added to session successfully.'}), 200

def page_not_found(e):
    """ Fonction utilisée si la mauvaise route est spécifiée par un(e) utilisateur(-trice)"""
    return "<h1>404</h1><p>La ressource n'a pas été trouvée.</p>", 404

def _format_name(name_raw):
    name = name_raw.capitalize()
    # Check if the name contain only allowed characters
    if not re.match(r'^[a-zA-Z-]+$', name):
        raise NameError('FirstName and LastName must contain only letters and hyphens.')

    # Check if the FirstName and LastName exceed the maximum length
    if len(name) > NAME_MAX_SIZE:
        raise NameError(f'FirstName and LastName must be {NAME_MAX_SIZE} characters or less.')
    
    return name

def _checkId(id):
    if not re.match(r'^[1-9]+$', id):
        raise NameError(f'id is not in correct format')

def _format_birth_date(birth_date):
    # Validate the birth date format
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', birth_date):
        raise NameError('Invalid birth date format. Expected yyyy-mm-dd.')

    # Convert the birth date string to a datetime object
    return datetime.strptime(birth_date, "%Y-%m-%d")
