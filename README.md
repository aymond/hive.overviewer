# Hive.Overviewer

A web application for managing game servers and their configurations.

## Features

- Manage multiple host servers
- Configure and monitor game servers
- Deploy and manage game configuration files
- User authentication and authorization

## Docker Deployment

### Prerequisites

- Docker
- Docker Compose

### Quick Start

1. Clone the repository:

```bash
git clone <repository-url>
cd hive.overviewer
```

2. Build and start the application:

```bash
docker-compose up -d
```

The application will be available at http://localhost:5000

3. View logs:

```bash
docker-compose logs -f
```

### Environment Variables

You can customize the application behavior through environment variables in the `docker-compose.yml` file:

- `FLASK_ENV`: Set to `development` or `production`
- `SECRET_KEY`: Secret key for session management (change for production)
- `DATABASE_URL`: Database connection string
- `GOOGLE_CLIENT_ID`: Your Google OAuth client ID (if using Google auth)
- `GOOGLE_CLIENT_SECRET`: Your Google OAuth client secret (if using Google auth)

### Production Deployment

For production deployment, modify the `docker-compose.yml` file:

```yaml
environment:
  - FLASK_ENV=production
  - OAUTHLIB_INSECURE_TRANSPORT=0  # Remove this line in production
  - APP_SETTINGS=config.ProductionConfig
  - SECRET_KEY=<your-secure-secret-key>
```

Consider setting up a proper database like PostgreSQL for production:

```yaml
services:
  web:
    # ... existing configuration ...
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/hive_overviewer
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=hive_overviewer
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Manual Setup (without Docker)

### Prerequisites

- Python 3.12+
- pip
- virtualenv

### Installation

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
export FLASK_APP=app
export FLASK_ENV=development
```

On Windows:
```cmd
set FLASK_APP=app
set FLASK_ENV=development
```

4. Initialize the database:

```bash
flask db upgrade
```

5. Run the application:

```bash
flask run
```

## Development

### Database Migrations

When you make changes to the models:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

### Testing

```bash
pytest
```

## License

[MIT License](LICENSE)
