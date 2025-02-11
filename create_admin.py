from app import create_app
from extensions import db
from models.user import User
import sys

def create_admin(username, password, email=None):
    app = create_app()
    
    with app.app_context():
        # Ensure database is created
        db.create_all()
        
        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user:
            # Update existing user to admin
            existing_user.is_admin = True
            existing_user.set_password(password)
            if email:
                existing_user.email = email
            db.session.commit()
            print(f"User {username} has been granted admin privileges.")
        else:
            # Create new admin user
            admin_user = User(
                username=username, 
                is_admin=True,
                email=email or f"{username}@example.com"
            )
            admin_user.set_password(password)
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user {username} has been created.")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python create_admin.py <username> <password> [email]")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    email = sys.argv[3] if len(sys.argv) > 3 else None
    
    create_admin(username, password, email)
