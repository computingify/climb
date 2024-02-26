import flask
from flask import request, jsonify
import sqlite3
import db
from datetime import datetime
import re
from email_validator import validate_email, EmailNotValidError

# Micro REST API creation
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create Data Base object
db = db.data_base()

# Definition du format de sortie
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# definition de l'ensemble des routes prises en charge par l'API
@app.route('/', methods=['GET'])
def home():
     return f'''<h1>Annuaire des employés</h1>
 <p>Prototype d'une API d'accès à la table employees de la base de données {db_name}.</p>'''
 
@app.route('/api/v1/resources/users/all', methods=['GET'])
def api_get_all_users():
    return jsonify(db.get_all_users())

@app.route('/api/v1/resources/user', methods=['PUT'])
def api_add_user():
    query_parameters = request.args
    print(f"parameters {query_parameters}")

    # Check if the FirstName and LastName contain only allowed characters
    first_name = query_parameters.get('FirstName').capitalize()
    last_name = query_parameters.get('LastName').capitalize()
    if not re.match(r'^[a-zA-Z-]+$', first_name) or not re.match(r'^[a-zA-Z-]+$', last_name):
        return jsonify({'error': 'FirstName and LastName must contain only letters and hyphens.'}), 400

    # Check if the FirstName and LastName exceed the maximum length
    if len(first_name) > 16 or len(last_name) > 16:
        return jsonify({'error': 'FirstName and LastName must be 16 characters or less.'}), 400

    # Validate the birth date format
    birth_date_str = query_parameters.get('BirthDate')
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', birth_date_str):
        return jsonify({'error': 'Invalid birth date format. Expected yyyy-mm-dd.'}), 400

    # Convert the birth date string to a datetime object
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")

    # Validate the email address format (if provided)
    email = query_parameters.get('email')
    if email:
        try:
            validate_email(email)
        except EmailNotValidError:
            return jsonify({'error': 'Invalid email address format.'}), 400

    # Store data into DB
    user_data = (first_name, last_name, birth_date, email)
    db.create_user(user_data)
    return jsonify("success")

def page_not_found(e):
    """ Fonction utilisée si la mauvaise route est spécifiée par un(e) utilisateur(-trice)"""
    return "<h1>404</h1><p>La ressource n'a pas été trouvée.</p>", 404

@app.route('/api/v1/resources/employees', methods=['GET'])
def api_filter():
    query_parameters = request.args
    print(f"parameters {query_parameters}")
    employeeid = query_parameters.get('EmployeeId')
    lastname = query_parameters.get('LastName')
    city = query_parameters.get('City')
    query = "SELECT * FROM employees WHERE 1=1"
    to_filter = []

    if employeeid:
        query += ' AND employeeid=?'
        to_filter.append(employeeid)
    if lastname:
        query += ' AND lastname=?'
        to_filter.append(lastname)
    if city:
        query += ' AND city=?'
        to_filter.append(city)

    conn = sqlite3.connect(db_name)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    print(f"query = {query}")
    all_employees = cur.execute(query, to_filter).fetchall()
    conn.close()
    return jsonify(all_employees)

@app.route('/api/v1/resources/employees', methods=['PUT'])
def api_add_presence():
    query_parameters = request.args
    print(f"parameters {query_parameters}")
    firstname = query_parameters.get('FirstName')
    lastname = query_parameters.get('LastName')
    to_filter = [firstname, lastname, 1]
    # Define the SQL statement with placeholders
    sql = """
        UPDATE employees
        SET Presence = ?
        WHERE FirstName = ? AND LastName = ?;
    """

    # Specify the new value for Presence and the specific FirstName and LastName values
    new_presence = 1

    # Execute the SQL statement with the specified parameters
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute(sql, (new_presence, firstname, lastname))

    # Commit the changes to the database
    conn.commit()

    # Close the connection
    conn.close()
    return jsonify("success")