from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=None):
    # Create and configure the app
    app = Flask(__name__)
    
    # Configure the app
    if config_class is None:
        app.config.from_object(os.getenv('APP_SETTINGS', 'config.DevelopmentConfig'))
    else:
        app.config.from_object(config_class)
    
    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Import and register blueprints
    from app.controllers.main import main_bp
    from app.controllers.auth import auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Import models to ensure user_loader is registered
    from app.models import user
    
    # Shell context for flask cli
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'app': app}
    
    return app
