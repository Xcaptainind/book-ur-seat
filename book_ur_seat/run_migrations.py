import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_ur_seat.settings')
django.setup()

print("Starting database migrations for Render...")
call_command('migrate', '--noinput')
print("Creating cache table if needed...")
call_command('createcachetable')
print("Database setup completed!")