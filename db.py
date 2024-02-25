import sqlite3

class data_base:
    def __init__(self) -> None:
        self.name = 'climb.db'
        self.users_table = 'users'
        self._create()

    def _create(self):
        conn = sqlite3.connect(self.name)
        # Create a cursor object
        cur = conn.cursor()

        sql_command = f'''CREATE TABLE IF NOT EXISTS {self.users_table} (
                            id INTEGER PRIMARY KEY,
                            FirstName TEXT,
                            LastName TEXT,
                            BirthDate TEXT,
                            email TEXT
                        )'''
        # Create a table
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
    
    def create_user(self, user_data):
        conn = sqlite3.connect(self.name)
        cur = conn.cursor()

        # Create or update the user
        sql_command = f'''INSERT OR REPLACE INTO {self.users_table} (id, FirstName, LastName, BirthDate, email)
                    VALUES ((SELECT id FROM {self.users_table} WHERE FirstName=? AND LastName=?), ?, ?, ?, ?)'''
        cur.execute(sql_command, (user_data[0], user_data[1], user_data[0], user_data[1], user_data[2], user_data[3]))

        conn.commit()
        conn.close()