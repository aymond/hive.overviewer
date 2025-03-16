from app import create_app, db
from app.models.user import User
import signal
import sys
import threading
import atexit

app = create_app()

# Store active threads for cleanup
active_threads = []

def cleanup_threads():
    """Cleanup function to stop all active threads"""
    print("\nStopping background threads...")
    for thread in active_threads:
        if hasattr(thread, 'stop'):
            thread.stop()
    print("All threads stopped.")

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print("\nReceived shutdown signal...")
    cleanup_threads()
    sys.exit(0)

@app.cli.command("init-db")
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Initialized the database.")

@app.cli.command("create-tables")
def create_tables():
    """Create all database tables."""
    db.create_all()
    print("Created all database tables.")

@app.cli.command("drop-tables")
def drop_tables():
    """Drop all database tables."""
    db.drop_all()
    print("Dropped all database tables.")

@app.cli.command("create-test-user")
def create_test_user():
    """Create a test user for development."""
    username = "testuser"
    email = "test@example.com"
    password = "password123"
    
    # Check if user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        print(f"Test user '{username}' already exists")
        return
    
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    print(f"Created test user: {username} with password: {password}")

if __name__ == '__main__':
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Register cleanup function
    atexit.register(cleanup_threads)
    
    # Run the app
    app.run(host='0.0.0.0', port=5000, use_reloader=True)
