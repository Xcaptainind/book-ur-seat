# movies/admin.py

from django.contrib import admin
from .models import (
    Movie, Theater, Seat, Booking,
    LiveEvent, EventCategory, EventBooking,
    EventSeat, EventSeatCategory
)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # This line tells the admin which fields to show in the add/edit form
    fields = ['name', 'image', 'rating', 'cast', 'description', 'genre', 'language', 'trailer_link']
    
    # This line controls the columns in the movie list view
    list_display = ['name', 'rating', 'genre', 'language']

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie', 'time']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['theater', 'seat_number', 'is_booked']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'seat', 'movie', 'theater', 'booked_at']

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(LiveEvent)
class LiveEventAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'event_date', 'venue', 'status', 'available_seats']
    list_filter = ['status', 'category', 'event_date']
    search_fields = ['name', 'venue', 'description']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'event_date'
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(EventSeatCategory)
class EventSeatCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']

@admin.register(EventSeat)
class EventSeatAdmin(admin.ModelAdmin):
    list_display = ['event', 'category', 'row', 'number', 'is_booked']
    list_filter = ['event', 'category', 'row', 'is_booked']
    search_fields = ['event__name']
    list_editable = ['is_booked']

@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'num_tickets', 'total_price', 'status', 'booking_date']
    list_filter = ['status', 'booking_date', 'event']
    search_fields = ['user__username', 'event__name']
    readonly_fields = ['booking_date']
    
    def get_seats(self, obj):
        return obj.get_seats_display()