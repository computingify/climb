import flask
from flask import request, jsonify
from db import data_base, UserNotFoundError
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from collections import namedtuple
from user import search_user
from tool import checkId, format_name, format_birth_date
from csv_importer import CsvImporter
from sqlInjectionChecker import SQLInjectionChecker

# Micro REST API creation
app = flask.Flask(__name__)
# Create Data Base object
db = data_base()
# SQL injection checker
checker = SQLInjectionChecker()

# Launch the application
if __name__ == '__main__':
    # app.config["DEBUG"] = False
    app.run(host='0.0.0.0', port=5000)

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
            id_val = search_user(db, first_name_val, last_name_val)
        if id_val is not None:
            checkId(id_val)
            user = db.is_user_id_exist(id_val)
            
    except NameError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify(user)

@app.route('/api/v1/resources/session/user/count', methods=['GET'])
def api_get_session_user_count():
    try:
        today = datetime.now().date().isoformat()
        count = db.get_session_user_count(today)
    except NameError as e:
        return jsonify({'error': str(e)}), 400
    
    return jsonify({'user_count': count})

@app.route('/api/v1/resources/summary', methods=['GET'])
def api_get_summary():
    try:
        climbers_per_session = db.get_users_per_session()
    except NameError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify(climbers_per_session)

@app.route('/api/v1/resources/user', methods=['POST'])
def api_add_user():

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
        first_name_val = format_name(first_name_val)
        last_name_val = format_name(last_name_val)
    except NameError as e:
        print(f'error {str(e)}')
        return jsonify({'error': str(e)}), 400
    
    # Validate the birth date format (if provided)
    if birth_date_str:
        try:
            birth_date_val = format_birth_date(birth_date_str)
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

@app.route('/api/v1/resources/session/add_user', methods=['POST'])
def api_add_user_to_session():
    
    # Get the user data from the request
    query_parameters = request.args
    user_id = query_parameters.get('UserId')
    safe = checker.is_safe(user_id)
    
    # Check if the user_id is provided
    if user_id is None or not safe:
        return jsonify({'error': 'UserId parameter is empty or not correct.'}), 400
    
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
    db.add_user_to_session(session_id, user_id)

    # Get number of User
    count_response = api_get_session_user_count()
    count_data = count_response.get_json()  # Extract JSON data from the response
    print(count_data)
    user_count = count_data.get('user_count', 0)
    # Return a success message
    return jsonify({'message': 'User added to session successfully.', 'count': user_count}), 200

@app.route('/api/v1/resources/user/import', methods=['POST'])
def api_import_users():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.csv'):
        importer = CsvImporter(db)
        importer.import_users(file)
        return jsonify({'message': 'Users imported successfully!'}), 200
    else:
        return jsonify({'error': 'Invalid file format. Please upload a CSV file.'}), 400

def page_not_found(e):
    """ Fonction utilisée si la mauvaise route est spécifiée par un(e) utilisateur(-trice)"""
    return "<h1>404</h1><p>La ressource n'a pas été trouvée.</p>", 404
