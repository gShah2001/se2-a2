from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__= "User"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role= db.Column(db.String(50), nullable= False, default= "user")

    def __init__(self, name, password, email, phone, role):
        self.name = name
        self.set_password(password)
        self.email = email
        self.phone = phone
        self.role = role

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.name}>'
