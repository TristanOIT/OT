from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

# Configure Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Specify the login route
login_manager.login_message_category = 'info'
