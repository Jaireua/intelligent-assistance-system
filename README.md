# Facial Authentication System

A secure authentication system that uses facial recognition technology to verify user identities. This system provides a modern, biometric approach to user authentication for web applications.

## Features

- **Facial Recognition Login**: Authenticate users by comparing their facial features with stored images
- **Secure Registration**: Register new users with their facial data
- **Django Admin Integration**: Manage users and facial data through the Django admin interface

## Technology Stack

- **Backend**: Django (Python web framework)
- **Facial Recognition**: face_recognition library
- **Database**: SQLite (default)
- **Frontend**: HTML, CSS, JavaScript

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Start the development server: `python manage.py runserver`

## Usage

- View signin page at `/`
- View login page at `/signin/`
- View admon page at the root URL `/admon/`

## Security Considerations

This system is currently configured for development purposes. For production use:
- Change the SECRET_KEY in settings.py
- Set DEBUG to False
- Configure proper ALLOWED_HOSTS
- Consider using a more robust database system