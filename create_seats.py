from django.core.management.base import BaseCommand
from movies.models import LiveEvent, EventSeatCategory, EventSeat

def create_seats():
    # Create seat category
    category = EventSeatCategory.objects.create(
        name='Regular',
        description='Regular seating',
        price=500.00
    )
    
    # Get the event
    event = LiveEvent.objects.get(slug='stant-up-comedt')
    
    # Create seats
    for row in 'ABCDEF':
        for number in range(1, 11):  # 1 to 10
            EventSeat.objects.create(
                event=event,
                category=category,
                row=row,
                number=number,
                is_booked=False
            )

if __name__ == '__main__':
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')
    django.setup()
    create_seats()