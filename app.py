from flask import Flask, render_template
from config import Config
from extensions import db, migrate, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.overtime import overtime_blueprint
    from routes.stock import stock_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(overtime_blueprint)
    app.register_blueprint(stock_bp)

    # Load the futuristic index page
    @app.route('/')
    def index():
        return render_template('index.html')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)