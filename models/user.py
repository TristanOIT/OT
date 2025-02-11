from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Role-based access control with explicit default values
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    can_access_overtime = db.Column(db.Boolean, default=False, nullable=False)
    can_access_inventory = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, password):
        """Create hashed password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password_hash, password)

    def has_overtime_access(self):
        """Check if user has overtime access."""
        return self.is_admin or self.can_access_overtime

    def has_inventory_access(self):
        """Check if user has inventory access."""
        return self.is_admin or self.can_access_inventory

    def __repr__(self):
        return f'<User {self.username}>'
