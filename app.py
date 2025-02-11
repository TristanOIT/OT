from flask import Flask, render_template
from flask_login import LoginManager
from extensions import db, migrate
from models.user import User
from models.overtime import OvertimeRequest

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register Blueprints
    from routes.auth import auth_bp
    from routes.overtime import overtime_blueprint
    from routes.admin import admin_blueprint
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(overtime_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    # Load the futuristic index page
    @app.route('/')
    def index():
        return render_template('index.html')
    
    # Create tables if not exists
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)