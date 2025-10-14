from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Event Categories"

class EventSeatCategory(models.Model):
    name = models.CharField(max_length=100)  # e.g., "VIP", "Regular", "Balcony"
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (₹{self.price})"

    class Meta:
        verbose_name_plural = "Event Seat Categories"

class LiveEvent(models.Model):
    EVENT_STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="events/")
    category = models.ForeignKey(EventCategory, on_delete=models.PROTECT)
    venue = models.CharField(max_length=255)
    venue_address = models.TextField()
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    price_from = models.DecimalField(max_digits=10, decimal_places=2)
    price_to = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=EVENT_STATUS_CHOICES, default='upcoming')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_available_seats(self, category=None):
        seats = EventSeat.objects.filter(event=self)
        if category:
            seats = seats.filter(category=category)
        return seats.filter(is_booked=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.available_seats and not self.id:
            self.available_seats = self.total_seats
        super().save(*args, **kwargs)

    @property
    def is_upcoming(self):
        return self.event_date > timezone.now().date()

class EventSeat(models.Model):
    ROW_CHOICES = [(chr(i), chr(i)) for i in range(65, 75)]  # A to J
    
    event = models.ForeignKey(LiveEvent, on_delete=models.CASCADE, related_name='seats')
    category = models.ForeignKey(EventSeatCategory, on_delete=models.PROTECT)
    row = models.CharField(max_length=1, choices=ROW_CHOICES)
    number = models.PositiveIntegerField()  # Seat number in row
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ['event', 'row', 'number']
        ordering = ['row', 'number']

    def __str__(self):
        return f"{self.event.name} - {self.row}{self.number} ({self.category.name})"

    @property
    def seat_label(self):
        return f"{self.row}{self.number}"

class EventBooking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    event = models.ForeignKey(LiveEvent, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    seats = models.ManyToManyField(EventSeat, related_name='bookings')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.user.username}'s booking for {self.event.name}"
    
    @property
    def num_tickets(self):
        return self.seats.count()
    
    def get_seats_display(self):
        return ", ".join(seat.seat_label for seat in self.seats.all())

# Updated Movie model with genre and language choices
class Movie(models.Model):
    # ... (no changes in this model) ...
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Horror', 'Horror'),
        ('Romance', 'Romance'),
        ('Sci-Fi', 'Sci-Fi'),
    ]

    LANGUAGE_CHOICES = [
        ('EN', 'English'),
        ('HI', 'Hindi'),
        ('TE', 'Telugu'),
        ('TA', 'Tamil'),
    ]

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="movies/")
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    cast = models.TextField()
    description = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, default='Action')
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='EN')
    trailer_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Theater(models.Model):
    name = models.CharField(max_length=255)
    # Change Movie to 'Movie'
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='theaters')
    time = models.DateTimeField()

    def __str__(self):
        return f'{self.name} - {self.movie.name} at {self.time}'

class Seat(models.Model):
    # Change Theater to 'Theater'
    theater = models.ForeignKey('Theater', on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.seat_number} in {self.theater.name}'

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Change Seat, Movie, and Theater to strings
    seat = models.OneToOneField('Seat', on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    theater = models.ForeignKey('Theater', on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking by {self.user.username} for {self.seat.seat_number} at {self.theater.name}'