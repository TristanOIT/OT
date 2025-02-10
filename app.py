from flask import Flask
from config import Config
from extensions import db, migrate, login_manager  # Import from extensions

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.overtime import overtime_bp
    from routes.stock import stock_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(overtime_bp)
    app.register_blueprint(stock_bp)

    # Simple index route
    @app.route('/')
    def index():
        return """
        <h1>Welcome to the Overtime and Stock Management Portal</h1>
        <p><a href='/login'>Login</a></p>
        """

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
