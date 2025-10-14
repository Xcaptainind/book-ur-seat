from django.core.management.base import BaseCommand
from movies.models import LiveEvent, EventSeatCategory, EventSeat

class Command(BaseCommand):
    help = 'Create seats for an event'

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int, help='ID of the event')
        parser.add_argument('category_id', type=int, help='ID of the seat category')

    def handle(self, *args, **options):
        event_id = options['event_id']
        category_id = options['category_id']

        try:
            event = LiveEvent.objects.get(id=event_id)
            category = EventSeatCategory.objects.get(id=category_id)

            # Create seats for rows A-J, numbers 1-10
            seats_created = 0
            for row in 'ABCDEFGHIJ':
                for number in range(1, 11):  # 1 to 10
                    EventSeat.objects.get_or_create(
                        event=event,
                        category=category,
                        row=row,
                        number=number
                    )
                    seats_created += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {seats_created} seats for event "{event.name}"'
                )
            )

        except LiveEvent.DoesNotExist:
            self.stdout.write(self.style.ERROR('Event not found'))
        except EventSeatCategory.DoesNotExist:
            self.stdout.write(self.style.ERROR('Seat category not found'))