# Python Web Application

A modern web application built with Python and Flask.

## Project Structure

```
.
├── app/                    # Application package
│   ├── __init__.py         # Package initializer
│   ├── controllers/        # Route handlers/controllers
│   │   ├── __init__.py
│   │   ├── auth.py         # Authentication routes
│   │   └── main.py         # Main routes
│   ├── models/             # Database models
│   │   ├── __init__.py
│   │   └── user.py         # User model
│   ├── static/             # Static files
│   │   ├── css/
│   │   │   └── styles.css  # Custom CSS
│   │   ├── js/
│   │   │   └── main.js     # Custom JavaScript
│   │   └── img/            # Images directory
│   ├── templates/          # HTML templates
│   │   ├── auth/
│   │   │   ├── login.html  # Login page template
│   │   │   └── register.html # Registration page template
│   │   ├── about.html      # About page template
│   │   ├── index.html      # Home page template
│   │   └── layout.html     # Base layout template
│   └── utils/              # Utility functions
│       └── __init__.py
├── config/                 # Configuration files
│   └── __init__.py         # Configuration settings
├── docs/                   # Documentation
├── tests/                  # Test cases
│   └── __init__.py
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore file
├── README.md               # Project documentation
├── requirements.txt        # Project dependencies
└── run.py                  # Application entry point
```

## Features

- User authentication (login/register)
- Google OAuth integration
- Responsive design with Bootstrap
- Database integration with SQLAlchemy
- CSRF protection
- Modular structure with Blueprints

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and update the variables:
   ```
   cp .env.example .env
   ```
5. Set up Google OAuth (optional):
   - Follow the instructions in `docs/google_oauth_setup.md`
   - Update the Google OAuth client ID and secret in your `.env` file
6. Initialize the database:
   ```
   python -c "from app import db, create_app; app = create_app(); app.app_context().push(); db.create_all()"
   ```
7. Run the application:
   ```
   python run.py
   ```

## Development

- Add your models in `app/models/`
- Add your route handlers in `app/controllers/`
- Add your HTML templates in `app/templates/`
- Add your static files in `app/static/`

## Authentication

The application supports two authentication methods:

1. **Traditional email/password authentication**
2. **Google OAuth authentication**

Users can register and log in using either method. If a user signs in with Google and their email already exists in the system, their account will be linked to their Google ID for future sign-ins.
