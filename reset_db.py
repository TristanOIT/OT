import os
import sys
import secrets

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models.user import User

def reset_database():
    """Reset the entire database and create initial admin user"""
    # Create Flask app context
    app = create_app()

    with app.app_context():
        # Drop all existing tables
        db.drop_all()

        # Recreate all tables
        db.create_all()

        # Create initial admin user
        initial_admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True,
            can_access_overtime=True,
            can_access_inventory=True
        )
        initial_admin.set_password('AdminPassword123!')

        # Add and commit the user
        db.session.add(initial_admin)
        db.session.commit()

        print("Database reset successfully.")
        print("Initial admin user created:")
        print(f"Username: {initial_admin.username}")
        print(f"Email: {initial_admin.email}")
        print("Password: AdminPassword123!")

if __name__ == '__main__':
    reset_database()
