from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

class User(UserMixin, db.Model):
    """User model for storing user data."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    google_id = db.Column(db.String(128), unique=True, nullable=True)
    preferences = db.Column(db.Text, nullable=True)  # JSON string for user preferences
    
    def __init__(self, username, email, password=None, google_id=None):
        self.username = username
        self.email = email
        self.google_id = google_id
        
        # Only set password if provided (not for OAuth users)
        if password:
            self.set_password(password)
        
        # Initialize default preferences
        self.set_default_preferences()
    
    def set_password(self, password):
        """Create hashed password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        if self.password_hash:
            return check_password_hash(self.password_hash, password)
        return False
    
    @property
    def is_oauth_user(self):
        """Check if user was created via OAuth."""
        return self.password_hash is None and self.google_id is not None
    
    def set_default_preferences(self):
        """Set default user preferences."""
        default_prefs = {
            'theme': 'light',
            'email_notifications': True,
            'push_notifications': False,
            'marketing_emails': False,
            'profile_visibility': True,
            'data_sharing': False
        }
        self.preferences = json.dumps(default_prefs)
    
    def get_preferences(self):
        """Get user preferences as a dictionary."""
        if not self.preferences:
            self.set_default_preferences()
            db.session.commit()
        
        return json.loads(self.preferences)
    
    def update_preferences(self, new_preferences):
        """Update user preferences."""
        current_prefs = self.get_preferences()
        current_prefs.update(new_preferences)
        self.preferences = json.dumps(current_prefs)
    
    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.query.get(int(user_id)) 