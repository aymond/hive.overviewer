# Python Web Application

A modern web application built with Python.

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
4. Copy `.env.example` to `.env` and update the variables
5. Run the application:
   ```
   python run.py
   ```

## Development

- Add your models in `app/models/`
- Add your route handlers in `app/controllers/`
- Add your HTML templates in `app/templates/`
- Add your static files in `app/static/`
