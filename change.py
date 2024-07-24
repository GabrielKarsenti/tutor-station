import os

from werkzeug.security import generate_password_hash

from app import User, app, db


def add_user(email, first_name, password):
    """Add a new user to the database."""
    with app.app_context():
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"User with email {email} already exists.")
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(email=email, first_name=first_name, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            print(f"User with email {email} added successfully.")

def update_user(email, new_password=None, new_first_name=None, new_hours_completed=None):
    """Update an existing user's information in the database."""
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            if new_password:
                user.password = generate_password_hash(new_password)
            if new_first_name:
                user.first_name = new_first_name
            if new_hours_completed is not None:
                user.hours_completed = new_hours_completed
            db.session.commit()
            print(f"User with email {email} updated successfully.")
        else:
            print(f"User with email {email} not found.")

def get_user_detail(email, detail):
    """Get specific details of a user from the database."""
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            if hasattr(user, detail):
                print(f"{detail} of user with email {email} is: {getattr(user, detail)}")
            else:
                print(f"User with email {email} does not have attribute {detail}")
        else:
            print(f"User with email {email} not found.")

def get_all_users():
    """Get hours_completed for all users."""
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(f"{user.email} - {user.hours_completed}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Add, update, or get users in the database.')
    parser.add_argument('--add', action='store_true', help='Add a new user')
    parser.add_argument('--update', action='store_true', help='Update an existing user')
    parser.add_argument('--get', action='store_true', help='Get a specific detail of a user')
    parser.add_argument('--all', action='store_true', help='Get hours_completed for all users')
    parser.add_argument('--email', type=str, help='Email of the user')
    parser.add_argument('--first_name', type=str, help='First name of the user')
    parser.add_argument('--password', type=str, help='Password of the user')
    parser.add_argument('--hours_completed', type=int, help='Hours completed by the user')
    parser.add_argument('--detail', type=str, help='Specific detail to get (e.g., first_name, hours_completed)')

    args = parser.parse_args()

    if args.add:
        if not args.first_name or not args.password:
            print("To add a new user, you must provide the first name and password.")
        else:
            add_user(args.email, args.first_name, args.password)
    elif args.update:
        if not (args.password or args.first_name or args.hours_completed is not None):
            print("To update a user, you must provide at least one field to update (password, first_name, or hours_completed).")
        else:
            update_user(args.email, args.password, args.first_name, args.hours_completed)
    elif args.get:
        if args.detail:
            get_user_detail(args.email, args.detail)
        else:
            print("To get a user detail, you must provide the detail to retrieve (first_name, hours_completed).")
    elif args.all:
        get_all_users()
    else:
        print("You must specify either --add, --update, --get, or --all.")



# FOR EXAMPLE --- UPDATE  --- """"   python change.py --update --email gabrielkarsenti@gmail.com --hours_completed 10    """"

# FOR EXAMPLE ---- GET ------ """"    python change.py --get --email gabrielkarsenti@gmail.com --detail hours_completed """""

# FOR EXAMPLE ---- ADD ------ """"    python change.py --add --email user@example.com --first_name "John" --password "password123"   """""

# FOR EXAMPLE ---- ALL ------ """"    python change.py --all """"
