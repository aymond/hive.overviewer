from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Allow OAuth over HTTP for development
if os.environ.get('FLASK_ENV') == 'development' or os.environ.get('APP_SETTINGS') == 'config.DevelopmentConfig':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()
session = Session()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

def create_app(config_class=None):
    # Create and configure the app
    app = Flask(__name__)
    
    # Initialize limiter
    limiter.init_app(app)
    
    # Apply rate limits to specific endpoints
    @app.before_request
    def apply_rate_limits():
        if request.endpoint:
            if 'auth.' in request.endpoint:
                limiter.limit("5 per minute")(lambda: None)()
            elif 'hosts.check_host_status' in request.endpoint:
                limiter.limit("10 per minute")(lambda: None)()
    
    # Configure the app
    if config_class is None:
        app.config.from_object(os.getenv('APP_SETTINGS', 'config.DevelopmentConfig'))
    else:
        app.config.from_object(config_class)
    
    # Configure session for Flask-Dance
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Security headers
    @app.after_request
    def add_security_headers(response):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: blob:; "
            "font-src 'self' data:;"
        )
        return response
    
    # OAuth configuration
    app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
    app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
    
    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    session.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Import and register blueprints
    from app.controllers.main import main_bp
    from app.controllers.auth import auth_bp
    from app.controllers.google_auth import google_auth_bp, google_bp
    from app.controllers.hosts import hosts_bp
    from app.controllers.game_servers import game_servers_bp
    from app.controllers.game_configs import game_configs_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(google_auth_bp, url_prefix='/auth')
    app.register_blueprint(google_bp, url_prefix='/login')
    app.register_blueprint(hosts_bp)
    app.register_blueprint(game_servers_bp)
    app.register_blueprint(game_configs_bp)
    
    # Setup user loader
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Shell context for flask cli
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'app': app}
    
    return app
