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
        sql_command = f'''CREATE TABLE IF NOT EXISTS {self.session_attendees_table} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id INTEGER NOT NULL,
                        user_id INTEGER NOT NULL,
                        date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(session_id, user_id),
                        FOREIGN KEY (session_id) REFERENCES {self.session_table}(id),
                        FOREIGN KEY (user_id) REFERENCES {self.users_table}(id)
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
    
    def add_user_to_session(self, session_id, user_id):
        conn = sqlite3.connect(self.name)
        cur = conn.cursor()
        print(f"Inserting into {self.session_attendees_table}: session_id={session_id}, user_id={user_id}")

        try:
            cur.execute(f"INSERT INTO {self.session_attendees_table} (session_id, user_id) VALUES (?, ?)", (session_id, user_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
            
    def get_users_per_session(self):
        conn = sqlite3.connect(self.name)
        cur = conn.cursor()

        # Query to join the user and sessions based on the session_attendees table
        query = """
        SELECT s.date, u.FirstName, u.LastName
        FROM session_attendees sa
        JOIN sessions s ON sa.session_id = s.id
        JOIN users u ON sa.user_id = u.id
        ORDER BY s.date, u.LastName, u.FirstName
        """

        cur.execute(query)
        results = cur.fetchall()

        # Organize the results into a dictionary: {session_date: [climber names]}
        sessions_summary = {}
        for session_date, first_name, last_name in results:
            if session_date not in sessions_summary:
                sessions_summary[session_date] = []
            sessions_summary[session_date].append(f"{first_name} {last_name}")

        conn.close()
        return sessions_summary
    
    def get_session_user_count(self, session_date):
        conn = sqlite3.connect(self.name)
        cur = conn.cursor()

        query = """
        SELECT COUNT(*)
        FROM session_attendees sa
        JOIN sessions s ON sa.session_id = s.id
        WHERE s.date = ?
        """
        cur.execute(query, (session_date,))
        count = cur.fetchone()[0]

        conn.close()
        return count