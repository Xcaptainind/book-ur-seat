from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('romance', 'Romance'),
        ('thriller', 'Thriller'),
        ('sci-fi', 'Science Fiction'),
        ('adventure', 'Adventure'),
        ('animation', 'Animation'),
        ('documentary', 'Documentary'),
    ]
    
    LANGUAGE_CHOICES = [
        ('hindi', 'Hindi'),
        ('english', 'English'),
        ('tamil', 'Tamil'),
        ('telugu', 'Telugu'),
        ('malayalam', 'Malayalam'),
        ('kannada', 'Kannada'),
        ('bengali', 'Bengali'),
        ('marathi', 'Marathi'),
    ]
    
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="movies/")
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(10)])
    cast = models.TextField()
    description = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='drama')
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='hindi')
    trailer_url = models.URLField(blank=True, null=True, help_text="YouTube trailer URL")
    duration = models.PositiveIntegerField(help_text="Duration in minutes", default=120)
    release_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Theater(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='theaters')
    time = models.DateTimeField()
    price_per_seat = models.DecimalField(max_digits=8, decimal_places=2, default=200.00)
    total_seats = models.PositiveIntegerField(default=100)
    available_seats = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f'{self.name} - {self.movie.name} at {self.time}'
    
    def save(self, *args, **kwargs):
        if not self.pk:  # New theater
            self.available_seats = self.total_seats
        super().save(*args, **kwargs)


class Seat(models.Model):
    SEAT_STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('booked', 'Booked'),
    ]
    
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=SEAT_STATUS_CHOICES, default='available')
    reserved_until = models.DateTimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.seat_number} in {self.theater.name}'
    
    @property
    def is_booked(self):
        return self.status == 'booked'
    
    @property
    def is_reserved(self):
        return self.status == 'reserved'


class SeatReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Reservation by {self.user.username} for {self.seat.seat_number} expires at {self.expires_at}'
    
    @property
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at


class Booking(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('stripe', 'Stripe'),
        ('razorpay', 'Razorpay'),
        ('cash', 'Cash'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    email_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Booking by {self.user.username} for {self.seat.seat_number} at {self.theater.name}'
    
    @property
    def total_amount(self):
        return self.seat.price or self.theater.price_per_seat