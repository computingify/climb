from flask import jsonify
from tool import similar

def search_user(db, first_name, last_name):
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
            first_name_score = similar(first_name, user[1].lower()) if first_name else 0
            last_name_score = similar(last_name, user[2].lower()) if last_name else 0
            twisted_first_name_score = similar(last_name, user[1].lower()) if last_name else 0
            twisted_last_name_score = similar(first_name, user[2].lower()) if first_name else 0
            score = first_name_score + last_name_score + twisted_first_name_score + twisted_last_name_score

            if score > best_score:
                best_score = score
                best_match = user

        return best_match

    best_match = find_best_match(first_name_val, last_name_val)

    # Handle the case where no match is found
    if not best_match:
        return jsonify({'error': f'No user found with FirstName: {first_name} and LastName: {last_name}'}), 404

    # Return the found user's ID if a match is found
    return str(best_match[0])
