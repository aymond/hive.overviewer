from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Handle login form submission here
    if request.method == 'POST':
        # Login logic would go here
        pass
        
    return render_template('auth/login.html', title='Login')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Handle registration form submission here
    if request.method == 'POST':
        # Registration logic would go here
        pass
        
    return render_template('auth/register.html', title='Register')

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page for editing profile information."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Check if username already exists (and is not the current user)
        if username != current_user.username:
            user_exists = User.query.filter_by(username=username).first()
            if user_exists:
                flash('Username already exists. Please choose a different one.', 'danger')
                return redirect(url_for('auth.profile'))
        
        # Check if email already exists (and is not the current user)
        if email != current_user.email:
            email_exists = User.query.filter_by(email=email).first()
            if email_exists:
                flash('Email already exists. Please use a different one.', 'danger')
                return redirect(url_for('auth.profile'))
        
        # Update user information
        current_user.username = username
        current_user.email = email
        
        # Update password if provided
        if new_password:
            if new_password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('auth.profile'))
            
            current_user.set_password(new_password)
            flash('Password updated successfully.', 'success')
        
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/profile.html', title='Edit Profile', user=current_user)

@auth_bp.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    """User preferences page."""
    if request.method == 'POST':
        # Get form data
        theme = request.form.get('theme', 'light')
        email_notifications = 'email_notifications' in request.form
        push_notifications = 'push_notifications' in request.form
        marketing_emails = 'marketing_emails' in request.form
        profile_visibility = 'profile_visibility' in request.form
        data_sharing = 'data_sharing' in request.form
        
        # Update user preferences
        preferences_data = {
            'theme': theme,
            'email_notifications': email_notifications,
            'push_notifications': push_notifications,
            'marketing_emails': marketing_emails,
            'profile_visibility': profile_visibility,
            'data_sharing': data_sharing
        }
        
        current_user.update_preferences(preferences_data)
        db.session.commit()
        
        flash('Preferences updated successfully.', 'success')
        return redirect(url_for('auth.preferences'))
    
    # Get user's current preferences
    user_prefs = current_user.get_preferences()
    
    return render_template('auth/preferences.html', title='User Preferences', prefs=user_prefs) 