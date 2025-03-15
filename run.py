from app import create_app, db
from app.models.user import User

app = create_app()

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
    app.run(host='0.0.0.0', port=5000)
