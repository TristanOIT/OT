from werkzeug.security import generate_password_hash
from models.user import User
from extensions import db
from app import create_app

app = create_app()

def add_user(username, password):
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)
    
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        print(f"User {username} added successfully.")

if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    add_user(username, password)