#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This script is the entry point for managing the Django project. It provides
access to various management commands such as running the development server,
creating database migrations, and more.
"""
import os
import sys


def main():
    """
    Run administrative tasks for the Django project.
    
    Sets up the Django environment, configures the settings module,
    and executes the command specified in the command line arguments.
    """
    # Set the default Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face_auth.settings')
    try:
        # Import Django's management module
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Provide error message if Django is not installed
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Execute the command
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
