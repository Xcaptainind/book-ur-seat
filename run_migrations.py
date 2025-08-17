import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_ur_seat.settings')
django.setup()

print("Starting database migrations...")
try:
    call_command('migrate', '--noinput')
    print("✅ Migrations completed successfully!")
except Exception as e:
    print(f"❌ Migration error: {str(e)}")
    exit(1)