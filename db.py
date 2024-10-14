import sqlite3

class UserNotFoundError(Exception):
    pass

class data_base:
    def __init__(self) -> None:
        self.name = 'climb.db'
        self.users_table = 'users'
        self.session_table = 'sessions'
        self.session_attendees_table = 'session_attendees'
        self._create()

    def _create(self):
        conn = sqlite3.connect(self.name)
        # Create a cursor object
        cur = conn.cursor()

        # Create users table
        sql_command = f'''CREATE TABLE IF NOT EXISTS {self.users_table} (
                        id INTEGER PRIMARY KEY,
                        FirstName TEXT,
                        LastName TEXT,
                        BirthDate TEXT,
                        email TEXT
                    )'''
        cur.execute(sql_command)

        # Create sessions table
        sql_command = f'''CREATE TABLE IF NOT EXISTS {self.session_table} (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        description TEXT
                    )'''
        cur.execute(sql_command)

        # Create attendees table
        cur.execute(f'''DROP TABLE IF EXISTS {self.session_attendees_table}''')
        sql_command = f'''CREATE TABLE IF NOT EXISTS {self.session_attendees_table} (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        session_id INTEGER,
                        date TEXT,
                        FOREIGN KEY (user_id) REFERENCES {self.users_table}(id),
                        FOREIGN KEY (session_id) REFERENCES {self.session_table}(id)
                    )'''
        cur.execute(sql_command)

        # Commit changes
        conn.commit()

        print("Data Base creation ended")

        conn.close()
    
    def get_all_users(self):
        conn = sqlite3.connect(self.name)
        cur = conn.cursor()
        sql_command = f'''SELECT * FROM {self.users_table}'''
        users = cur.execute(sql_command).fetchall()
        conn.close()
        return users
    
    def get_user(self, user_data):
        conn = sqlite3.connect(self.name)
        cur = conn.cursor()
        sql_command = f'''SELECT * FROM {self.users_table} WHERE 1=1 AND FirstName=? AND LastName=?'''
        users = cur.execute(sql_command, user_data).fetchall()
        conn.close()
        return users

    
    def create_user(self, user_data):
        conn = sqlite3.connect(self.name)
        cur = conn.cursor()

        # Create or update the user
        sql_command = f'''INSERT OR REPLACE INTO {self.users_table} (id, FirstName, LastName, BirthDate, email)
                    VALUES ((SELECT id FROM {self.users_table} WHERE FirstName=? AND LastName=?), ?, ?, ?, ?)'''
        cur.execute(sql_command, (user_data.first_name, user_data.last_name, user_data.first_name, user_data.last_name, user_data.birth_date, user_data.email))

        conn.commit()
        conn.close()
        
    def is_user_id_exist(self, id):
        conn = sqlite3.connect(self.name)
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM {self.users_table} WHERE id=?", id)
        user = cur.fetchone()
        
        if user is None:
            raise UserNotFoundError(f"User with ID {id} not found.")
        
        conn.close()
        ret = {
            'id': user[0],
            'first_name': user[1],
            'last_name': user[2],
            }
        
        return ret
    
    def get_session(self, date):
        conn = sqlite3.connect(self.name)
        cur = conn.cursor()
        
        cur.execute(f"SELECT * FROM {self.session_table} WHERE date=?", (date,))
        session = cur.fetchone()
        
        if session is None:
            # Create a new session for the current day if it does not exist
            cur.execute(f"INSERT INTO {self.session_table} (date) VALUES (?)", (date,))
            conn.commit()

            # Get the ID of the newly created session
            session_id = cur.lastrowid
        else:
            session_id = session[0]
        
        conn.close()
        
        return session_id
    
    def add_user_to_session(self, session_id, user_id, date):
        conn = sqlite3.connect(self.name)
        cur = conn.cursor()
        print(f"Inserting into {self.session_attendees_table}: session_id={session_id}, user_id={user_id}, date={date}")

        try:
            cur.execute(f"INSERT INTO {self.session_attendees_table} (session_id, user_id, date) VALUES (?, ?, ?)", (session_id, user_id, date))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()