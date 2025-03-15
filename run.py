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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
