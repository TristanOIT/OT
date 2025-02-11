import os
import secrets
from flask import Flask
from extensions import db, migrate, login_manager
from models.user import User

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Configure login view
    login_manager.login_view = 'auth.login'
    
    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.main import main_blueprint
    from routes.overtime import overtime_blueprint
    from routes.stock import stock_bp
    from routes.admin import admin_blueprint
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(overtime_blueprint)
    app.register_blueprint(stock_bp)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    # Create tables if not exists
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()