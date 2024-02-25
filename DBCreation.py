import sqlite3


def create_data_base():
    # Connect to the database
    conn = sqlite3.connect('climb.db')

    # Create a cursor object
    cur = conn.cursor()

    # Create a table
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    FirstName TEXT,
                    LastName TEXT,
                    BirthDate TEXT,
                    email TEXT
                )''')

    # Commit changes
    conn.commit()

    # Close the connection
    conn.close()