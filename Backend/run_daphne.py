import os
import django
from django.core.asgi import get_asgi_application

# Set the Django settings module path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django
django.setup()

# Import and run Daphne
from daphne.cli import CommandLineInterface

if __name__ == "__main__":
    cli = CommandLineInterface()
    cli.run(['config.asgi:application', '-b', '0.0.0.0', '-p', '8000']) 