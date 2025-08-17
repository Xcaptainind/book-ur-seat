
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Theater, Seat, Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth.forms import PasswordChangeForm
from users.forms import UserUpdateForm

def movie_list(request):
    search_query = request.GET.get('search')
    if search_query:
        movies = Movie.objects.filter(name__icontains=search_query)
    else:
        movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theaters = Theater.objects.filter(movie=movie)
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theaters})

@login_required(login_url='/login/')
def book_seats(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theater)
    
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        error_seats = []
        
        if not selected_seats:
            return render(request, "movies/seat_selection.html", {
                'theater': theater, 
                "seats": seats, 
                'error': "No seat selected"
            })
        
        for seat_id in selected_seats:
            seat = get_object_or_404(Seat, id=seat_id, theater=theater)
            
            # Check if seat is already booked using the status field
            if hasattr(seat, 'status') and seat.status in ['booked', 'reserved']:
                error_seats.append(seat.seat_number)
                continue
            elif hasattr(seat, 'is_booked') and seat.is_booked:
                error_seats.append(seat.seat_number)
                continue
                
            try:
                Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theater.movie,
                    theater=theater
                )
                # Update seat status
                if hasattr(seat, 'status'):
                    seat.status = 'booked'
                elif hasattr(seat, 'is_booked'):
                    seat.is_booked = True
                seat.save()
            except IntegrityError:
                error_seats.append(seat.seat_number)
        
        if error_seats:
            error_message = f"The following seats are already booked: {', '.join(error_seats)}"
            return render(request, 'movies/seat_selection.html', {
                'theater': theater, 
                "seats": seats, 
                'error': error_message
            })
        
        return redirect('profile')
    
    return render(request, 'movies/seat_selection.html', {'theater': theater, "seats": seats})

@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'u_form': u_form, 'bookings': bookings})

@login_required
def reset_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'users/reset_password.html', {'form': form})
