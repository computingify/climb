# Import des modules et fonctions Flask
import flask
from flask import request, jsonify

# Import de SQLite
import sqlite3

# Instantiation de l'application
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Definition du format de sortie
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# definition de l'ensemble des routes prises en charge par l'API
@app.route('/', methods=['GET'])
def home():
     return '''<h1>Annuaire des employés</h1>
 <p>Prototype d'une API d'accès à la table employees de la base de données Chinook.</p>'''
 
@app.route('/api/v1/resources/employees/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('chinook.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_employees = cur.execute('SELECT * FROM employees').fetchall()
    conn.close()
    return jsonify(all_employees)

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

    conn = sqlite3.connect('chinook.db')
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
    conn = sqlite3.connect('chinook.db')
    cur = conn.cursor()
    cur.execute(sql, (new_presence, firstname, lastname))

    # Commit the changes to the database
    conn.commit()

    # Close the connection
    conn.close()
    return jsonify("success")