from App.models import User
from App.database import db
from sqlalchemy.exc import IntegrityError

#def create_user(name, password, email, phone, role):
#    existing_user = User.query.filter_by(email=email).first()
#    if existing_user:
#        raise ValueError(f"A user with email {email} already exists.")
#    new_user = User(name=name, password=password, email=email, phone=phone, role=role)
#    db.session.add(new_user)
#    db.session.commit()
#    return new_user

def create_user(name, email, phone, password, role):
    try:
        # Create a new User instance
        new_user = User(name=name, email=email, phone=phone, password=password, role=role)
        
        # Add the new user to the session
        db.session.add(new_user)
        
        # Commit the session to save changes to the database
        db.session.commit()
        
        print("User  created successfully.")
    except IntegrityError:
        # Rollback the session in case of error
        db.session.rollback()
        print("Email already exists. Please use a different email.")
    except Exception as e:
        # Handle any other exceptions
        db.session.rollback()
        print(f"An error occurred: {str(e)}")

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    