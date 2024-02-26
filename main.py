import flask
from flask import request, jsonify
import sqlite3
import db
from datetime import datetime
import re
from email_validator import validate_email, EmailNotValidError
from collections import namedtuple

NAME_MAX_SIZE = 16

# Micro REST API creation
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create Data Base object
db = db.data_base()

# definition de l'ensemble des routes prises en charge par l'API
@app.route('/', methods=['GET'])
def home():
     return f'''<h1>Annuaire des employés</h1>
 <p>Prototype d'une API d'accès à la table employees de la base de données {db_name}.</p>'''
 
@app.route('/api/v1/resources/users/all', methods=['GET'])
def api_get_all_users():
    return jsonify(db.get_all_users())

@app.route('/api/v1/resources/user', methods=['GET'])
def api_get_user():
    query_parameters = request.args

    # Check if the FirstName and LastName contain only allowed characters
    first_name_val = query_parameters.get('FirstName').capitalize()
    last_name_val = query_parameters.get('LastName').capitalize()
    if first_name_val is None or last_name_val is None:
        return jsonify({'error': 'FirstName and LastName are required parameters.'}), 400

    try:
        first_name_val = _format_name(first_name_val)
        last_name_val = _format_name(last_name_val)
    except NameError as e:
        return jsonify({'error': str(e)}), 400

    user_data_format = namedtuple('User', ['first_name', 'last_name'])
    user_data = user_data_format(first_name=first_name_val, last_name=last_name_val)
    user = db.get_user(user_data)

    return jsonify(user)

@app.route('/api/v1/resources/user', methods=['PUT'])
def api_add_user():
    query_parameters = request.args

    # Validate FirstName and LastName format
    first_name_val = query_parameters.get('FirstName')
    last_name_val = query_parameters.get('LastName')
    
    if first_name_val is None or last_name_val is None:
        return jsonify({'error': 'FirstName and LastName are required parameters.'}), 400

    try:
        first_name_val = _format_name(first_name_val)
        last_name_val = _format_name(last_name_val)
    except NameError as e:
        return jsonify({'error': str(e)}), 400
    
    # Validate the birth date format (if provided)
    birth_date_str = query_parameters.get('BirthDate')
    if birth_date_str:
        try:
            birth_date_val = _format_birth_date(birth_date_str)
        except NameError as e:
            return jsonify({'error': str(e)}), 400

    # Validate the email address format (if provided)
    email_val = query_parameters.get('email')
    if email_val:
        try:
            validate_email(email_val)
        except EmailNotValidError:
            return jsonify({'error': 'Invalid email address format.'}), 400

    # Store data into DB
    user_data_format = namedtuple('User', ['first_name', 'last_name', 'birth_date', 'email'])
    user_data = user_data_format(first_name=first_name_val, last_name=last_name_val, birth_date=birth_date_val, email=email_val)
    db.create_user(user_data)
    return jsonify("success")

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

def _format_birth_date(birth_date):
    # Validate the birth date format
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', birth_date):
        raise NameError('Invalid birth date format. Expected yyyy-mm-dd.')

    # Convert the birth date string to a datetime object
    return datetime.strptime(birth_date, "%Y-%m-%d")