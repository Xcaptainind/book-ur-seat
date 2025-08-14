from django.contrib import admin
from .models import Movie, Theater, Seat, Booking, SeatReservation, Genre, Language


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'genre', 'language', 'duration', 'release_date', 'is_active']
    list_filter = ['genre', 'language', 'is_active', 'release_date']
    search_fields = ['name', 'cast', 'description']
    list_editable = ['is_active', 'rating']
    readonly_fields = ['rating']


@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie', 'time', 'location', 'price_per_seat', 'available_seats']
    list_filter = ['movie', 'time']
    search_fields = ['name', 'location']
    readonly_fields = ['available_seats']


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['theater', 'seat_number', 'status', 'price']
    list_filter = ['status', 'theater']
    search_fields = ['seat_number', 'theater__name']
    list_editable = ['status', 'price']


@admin.register(SeatReservation)
class SeatReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'seat', 'theater', 'reserved_at', 'expires_at', 'is_active']
    list_filter = ['is_active', 'reserved_at']
    search_fields = ['user__username', 'seat__seat_number']
    readonly_fields = ['reserved_at', 'expires_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'seat', 'movie', 'theater', 'booked_at', 'payment_status', 'amount_paid']
    list_filter = ['payment_status', 'payment_method', 'booked_at']
    search_fields = ['user__username', 'transaction_id']
    readonly_fields = ['booked_at', 'total_amount']
    list_editable = ['payment_status']
