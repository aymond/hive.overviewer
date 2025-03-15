from flask import Blueprint, redirect, url_for, current_app, flash, session
from flask_login import current_user, login_user, logout_user
from flask_dance.contrib.google import make_google_blueprint, google
from werkzeug.urls import url_parse
from sqlalchemy.orm.exc import NoResultFound
from app import db
from app.models.user import User

# Create blueprint for Google OAuth
google_bp = make_google_blueprint(
    scope=["profile", "email"],
    redirect_to="google_auth.google_login_callback"
)

google_auth_bp = Blueprint('google_auth', __name__)

@google_auth_bp.route('/login/google')
def google_login():
    """Redirect to Google for OAuth login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    return redirect(url_for('google.login'))

@google_auth_bp.route('/login/google/callback')
def google_login_callback():
    """Handle the callback from Google OAuth"""
    if not google.authorized:
        flash('Failed to log in with Google.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get info from Google
    resp = google.get('/oauth2/v1/userinfo')
    if not resp.ok:
        flash('Failed to get user info from Google.', 'danger')
        return redirect(url_for('auth.login'))
    
    google_info = resp.json()
    google_user_id = google_info['id']
    email = google_info['email']
    username = email.split('@')[0]  # Use part before @ as username
    
    # Check if this Google account is already linked to a user
    try:
        user = User.query.filter_by(google_id=google_user_id).one()
    except NoResultFound:
        # Check if a user with this email already exists
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Link the Google account to the existing user
            user.google_id = google_user_id
            db.session.commit()
        else:
            # Create a new user with the Google account info
            user = User(
                username=username,
                email=email,
                password=None,  # No password for Google users
                google_id=google_user_id
            )
            db.session.add(user)
            db.session.commit()
    
    # Log in the user
    login_user(user)
    flash(f'Successfully logged in as {user.username}', 'success')
    
    # Handle next URL
    next_page = session.get('next', None)
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('main.index')
    
    return redirect(next_page) 