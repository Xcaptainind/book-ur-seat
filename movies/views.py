from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta
from .models import (
    Movie, Theater, Seat, Booking,
    LiveEvent, EventCategory, EventBooking
)

# New function to handle the movie detail page
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies/movie_detail.html', {'movie': movie})

def list_view(request):
    """
    Dynamic view that shows either movies or events based on the URL namespace
    """
    if request.resolver_match.namespace == 'events':
        # Show events
        events = LiveEvent.objects.all().order_by('event_date')
        categories = EventCategory.objects.all()
        
        selected_category = request.GET.get('category')
        search_query = request.GET.get('search')
        date_filter = request.GET.get('date')

        if selected_category:
            events = events.filter(category__slug=selected_category)
        
        if search_query:
            events = events.filter(name__icontains=search_query)
        
        if date_filter:
            if date_filter == 'today':
                events = events.filter(event_date=timezone.now().date())
            elif date_filter == 'tomorrow':
                events = events.filter(event_date=timezone.now().date() + timezone.timedelta(days=1))
            elif date_filter == 'this_weekend':
                today = timezone.now().date()
                saturday = today + timezone.timedelta((5 - today.weekday()) % 7)
                sunday = saturday + timezone.timedelta(days=1)
                events = events.filter(event_date__range=[saturday, sunday])

        context = {
            'events': events,
            'categories': categories,
        }
        return render(request, 'events/event_list.html', context)
    
    else:
        # Show movies
        movies = Movie.objects.order_by('-id')
        genres = Movie.objects.values_list('genre', flat=True).distinct()
        languages = Movie.objects.values_list('language', flat=True).distinct()

        selected_genre = request.GET.get('genre')
        selected_language = request.GET.get('language')
        search_query = request.GET.get('search')

        if selected_genre:
            movies = movies.filter(genre=selected_genre)
        
        if selected_language:
            movies = movies.filter(language=selected_language)

        if search_query:
            movies = movies.filter(name__icontains=search_query)

        context = {
            'movies': movies,
            'genres': genres,
            'languages': languages,
        }
        return render(request, 'movies/movie_list.html', context)

def theater_list(request,movie_id):
    movie = get_object_or_404(Movie,id=movie_id)
    theater=Theater.objects.filter(movie=movie)
    return render(request,'movies/theater_list.html',{'movie':movie,'theaters':theater})



@login_required(login_url='/login/')
def book_seats(request,theater_id):
    theaters=get_object_or_404(Theater,id=theater_id)
    seats=Seat.objects.filter(theater=theaters)
    if request.method=='POST':
        selected_Seats= request.POST.getlist('seats')
        error_seats=[]
        if not selected_Seats:
            return render(request,"movies/seat_selection.html",{'theater':theaters,"seats":seats,'error':"No seat selected"})
        
        bookings_created = []
        for seat_id in selected_Seats:
            seat=get_object_or_404(Seat,id=seat_id,theater=theaters)
            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue
            try:
                booking = Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theaters.movie,
                    theater=theaters
                )
                bookings_created.append(booking)
                seat.is_booked=True
                seat.save()
            except IntegrityError:
                error_seats.append(seat.seat_number)
        
        if error_seats:
            error_message=f"The following seats are already booked:{','.join(error_seats)}"
            return render(request,'movies/seat_selection.html',{'theater':theaters,"seats":seats,'error':error_message})
        
        # Prepare booking data for email confirmation
        booking_data = {
            'userEmail': request.user.email,
            'userName': request.user.username,
            'movieName': theaters.movie.name,
            'theaterName': theaters.name,
            'showTime': theaters.time.strftime('%Y-%m-%d %H:%M'),
            'seatNumbers': [booking.seat.seat_number for booking in bookings_created],
            'bookingDate': bookings_created[0].booked_at.strftime('%Y-%m-%d %H:%M') if bookings_created else '',
            'bookingId': bookings_created[0].id if bookings_created else '',
            'totalAmount': 'N/A'  # Movie bookings don't have pricing in current model
        }
        
        return render(request, 'movies/booking_success.html', {
            'theater': theaters,
            'bookings': bookings_created,
            'booking_data': booking_data
        })
    return render(request,'movies/seat_selection.html',{'theaters':theaters,"seats":seats})

# Live Events Views
def event_list(request):
    events = LiveEvent.objects.all().order_by('event_date')
    categories = EventCategory.objects.all()
    
    selected_category = request.GET.get('category')
    search_query = request.GET.get('search')
    date_filter = request.GET.get('date')

    if selected_category:
        events = events.filter(category__slug=selected_category)
    
    if search_query:
        events = events.filter(name__icontains=search_query)
    
    if date_filter:
        if date_filter == 'today':
            events = events.filter(event_date=timezone.now().date())
        elif date_filter == 'tomorrow':
            events = events.filter(event_date=timezone.now().date() + timezone.timedelta(days=1))
        elif date_filter == 'this_weekend':
            # Get next Saturday and Sunday
            today = timezone.now().date()
            saturday = today + timezone.timedelta((5 - today.weekday()) % 7)
            sunday = saturday + timezone.timedelta(days=1)
            events = events.filter(event_date__range=[saturday, sunday])

    context = {
        'events': events,
        'categories': categories,
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, event_slug):
    event = get_object_or_404(LiveEvent, slug=event_slug)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required(login_url='/login/')
def book_event(request, event_slug):
    event = get_object_or_404(LiveEvent, slug=event_slug)
    from .models import EventSeatCategory, EventSeat
    
    # Get all seat categories
    seat_categories = EventSeatCategory.objects.all()
    # Get all seats for this event
    seats = EventSeat.objects.filter(event=event).select_related('category')
    
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        
        if not selected_seats:
            return render(request, 'events/event_booking.html', {
                'event': event,
                'seat_categories': seat_categories,
                'seats': seats,
                'error': "Please select at least one seat"
            })
        
        # Calculate total price based on selected seats
        total_price = sum(
            seat.category.price 
            for seat in seats.filter(id__in=selected_seats)
        )
        
        try:
            # Create the booking
            booking = EventBooking.objects.create(
                event=event,
                user=request.user,
                total_price=total_price,
                status='confirmed'
            )
            
            # Add selected seats to the booking
            booking.seats.set(selected_seats)
            
            # Mark seats as booked
            seats.filter(id__in=selected_seats).update(is_booked=True)
            
            # Update available seats count
            event.available_seats = event.get_available_seats().count()
            event.save()
            
            # Prepare booking data for email confirmation
            booking_data = {
                'userEmail': request.user.email,
                'userName': request.user.username,
                'eventName': event.name,
                'eventDate': event.event_date.strftime('%Y-%m-%d'),
                'eventTime': event.start_time.strftime('%H:%M'),
                'venue': event.venue,
                'seatNumbers': [seat.seat_label for seat in booking.seats.all()],
                'bookingDate': booking.booking_date.strftime('%Y-%m-%d %H:%M'),
                'bookingId': booking.id,
                'totalAmount': total_price
            }
            
            return render(request, 'events/booking_success.html', {
                'event': event,
                'booking': booking,
                'booking_data': booking_data
            })
            
        except Exception as e:
            return render(request, 'events/event_booking.html', {
                'event': event,
                'seat_categories': seat_categories,
                'seats': seats,
                'error': "An error occurred during booking. Please try again."
            })
    
    context = {
        'event': event,
        'seat_categories': seat_categories,
        'seats': seats,
    }
    return render(request, 'events/event_booking.html', context)