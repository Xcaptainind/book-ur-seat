import os
import sys
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_ur_seat.settings')

# Import the Django WSGI application
from book_ur_seat.wsgi import application

# This is the WSGI application that Render will use
app = application
