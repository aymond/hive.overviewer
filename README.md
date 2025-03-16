# Hive Overviewer

A web application for managing and monitoring game servers.

## Description

Hive Overviewer is a modern web application that helps you manage and monitor multiple game servers across different hosts. It provides an intuitive interface for server management, configuration, and status monitoring.

## Features

- Host management with status monitoring
- Game server deployment and configuration
- Real-time server status updates
- Configuration file management
- User authentication and authorization
- Modern, responsive design

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hive.overviewer.git
cd hive.overviewer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up the environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Run the application:
```bash
flask run
```

## Usage

Visit `http://localhost:5000` in your web browser to access the application.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Third-Party Licenses

This project includes several third-party open source components:

- **Bootstrap** (MIT License)
  - Copyright (c) 2011-2024 The Bootstrap Authors
  - https://getbootstrap.com
  - Used for core CSS and JavaScript functionality

- **Bootstrap Icons** (MIT License)
  - Copyright (c) 2019-2024 The Bootstrap Authors
  - https://icons.getbootstrap.com
  - Used for iconography throughout the application

For full license texts and notices, please see the [NOTICE](NOTICE) file.

## Acknowledgments

- Bootstrap team for their excellent framework and icons
- All contributors who have helped with the project
