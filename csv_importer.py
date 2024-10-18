import csv
from collections import namedtuple

class CsvImporter:
    def __init__(self, db):
        self.db = db

    def import_users(self, file_storage):
         # Use the file_storage directly instead of trying to open it
        reader = csv.reader(file_storage.stream.read().decode('utf-8').splitlines())

        # Skip the header row if needed
        next(reader)

        User = namedtuple('User', ['first_name', 'last_name', 'birth_date', 'email'])

        for row in reader:
            if len(row) != 4:
                raise ValueError("Each row must contain exactly 4 columns: FirstName, LastName, BirthDate, Email.")

            # Create user data tuple
            user_data = User(first_name=row[0], last_name=row[1], birth_date=row[2], email=row[3])
            self.db.create_user(user_data)  # Assuming create_user method can handle this data structure