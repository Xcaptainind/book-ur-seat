from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Movie, Theater, Seat, Booking, SeatReservation
from django.contrib.auth.models import User
import json


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with analytics and metrics"""
    
    # Date range for analytics (last 30 days)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    # Revenue analytics
    total_revenue = Booking.objects.filter(
        payment_status='completed',
        booked_at__range=[start_date, end_date]
    ).aggregate(total=Sum('amount_paid'))['total'] or 0
    
    monthly_revenue = Booking.objects.filter(
        payment_status='completed',
        booked_at__range=[start_date, end_date]
    ).aggregate(total=Sum('amount_paid'))['total'] or 0
    
    # Booking analytics
    total_bookings = Booking.objects.filter(
        booked_at__range=[start_date, end_date]
    ).count()
    
    completed_bookings = Booking.objects.filter(
        payment_status='completed',
        booked_at__range=[start_date, end_date]
    ).count()
    
    pending_bookings = Booking.objects.filter(
        payment_status='pending',
        booked_at__range=[start_date, end_date]
    ).count()
    
    # Movie popularity
    popular_movies = Movie.objects.annotate(
        booking_count=Count('theaters__seats__booking')
    ).order_by('-booking_count')[:5]
    
    # Theater performance
    theater_performance = Theater.objects.annotate(
        booking_count=Count('seats__booking'),
        revenue=Sum('seats__booking__amount_paid')
    ).filter(booking_count__gt=0).order_by('-revenue')[:5]
    
    # User analytics
    active_users = User.objects.annotate(
        booking_count=Count('booking')
    ).filter(booking_count__gt=0).count()
    
    # Seat utilization
    total_seats = Seat.objects.count()
    booked_seats = Seat.objects.filter(status='booked').count()
    reserved_seats = Seat.objects.filter(status='reserved').count()
    available_seats = total_seats - booked_seats - reserved_seats
    
    seat_utilization = {
        'total': total_seats,
        'booked': booked_seats,
        'reserved': reserved_seats,
        'available': available_seats,
        'utilization_percentage': round((booked_seats / total_seats * 100) if total_seats > 0 else 0, 2)
    }
    
    # Daily revenue chart data
    daily_revenue = []
    for i in range(30):
        date = end_date - timedelta(days=i)
        day_revenue = Booking.objects.filter(
            payment_status='completed',
            booked_at__date=date.date()
        ).aggregate(total=Sum('amount_paid'))['total'] or 0
        daily_revenue.append({
            'date': date.strftime('%Y-%m-%d'),
            'revenue': float(day_revenue)
        })
    
    daily_revenue.reverse()  # Show oldest to newest
    
    # Genre distribution
    genre_distribution = {}
    for choice in Movie.GENRE_CHOICES:
        genre_name = choice[1]
        genre_count = Movie.objects.filter(genre=choice[0]).count()
        genre_distribution[genre_name] = genre_count
    
    # Language distribution
    language_distribution = {}
    for choice in Movie.LANGUAGE_CHOICES:
        language_name = choice[1]
        language_count = Movie.objects.filter(language=choice[0]).count()
        language_distribution[language_name] = language_count
    
    # Recent activities
    recent_bookings = Booking.objects.select_related(
        'user', 'movie', 'theater', 'seat'
    ).order_by('-booked_at')[:10]
    
    recent_reservations = SeatReservation.objects.select_related(
        'user', 'theater', 'seat'
    ).filter(is_active=True).order_by('-reserved_at')[:10]
    
    context = {
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'total_bookings': total_bookings,
        'completed_bookings': completed_bookings,
        'pending_bookings': pending_bookings,
        'popular_movies': popular_movies,
        'theater_performance': theater_performance,
        'active_users': active_users,
        'seat_utilization': seat_utilization,
        'daily_revenue': json.dumps(daily_revenue),
        'genre_distribution': json.dumps(genre_distribution),
        'language_distribution': json.dumps(language_distribution),
        'recent_bookings': recent_bookings,
        'recent_reservations': recent_reservations,
        'date_range': {
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d')
        }
    }
    
    return render(request, 'movies/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def revenue_report(request):
    """Detailed revenue report"""
    
    # Get date range from request
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    else:
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
    
    # Revenue by payment method
    revenue_by_method = Booking.objects.filter(
        payment_status='completed',
        booked_at__range=[start_date, end_date]
    ).values('payment_method').annotate(
        total_revenue=Sum('amount_paid'),
        booking_count=Count('id')
    ).order_by('-total_revenue')
    
    # Revenue by movie
    revenue_by_movie = Booking.objects.filter(
        payment_status='completed',
        booked_at__range=[start_date, end_date]
    ).values('movie__name').annotate(
        total_revenue=Sum('amount_paid'),
        booking_count=Count('id')
    ).order_by('-total_revenue')
    
    # Revenue by theater
    revenue_by_theater = Booking.objects.filter(
        payment_status='completed',
        booked_at__range=[start_date, end_date]
    ).values('theater__name').annotate(
        total_revenue=Sum('amount_paid'),
        booking_count=Count('id')
    ).order_by('-total_revenue')
    
    # Daily revenue breakdown
    daily_revenue = []
    current_date = start_date
    while current_date <= end_date:
        day_revenue = Booking.objects.filter(
            payment_status='completed',
            booked_at__date=current_date.date()
        ).aggregate(total=Sum('amount_paid'))['total'] or 0
        
        daily_revenue.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'revenue': float(day_revenue)
        })
        current_date += timedelta(days=1)
    
    context = {
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'revenue_by_method': revenue_by_method,
        'revenue_by_movie': revenue_by_movie,
        'revenue_by_theater': revenue_by_theater,
        'daily_revenue': json.dumps(daily_revenue),
    }
    
    return render(request, 'movies/revenue_report.html', context)


@login_required
@user_passes_test(is_admin)
def user_analytics(request):
    """User behavior and analytics"""
    
    # User registration over time
    end_date = timezone.now()
    start_date = end_date - timedelta(days=90)
    
    user_registration_data = []
    current_date = start_date
    while current_date <= end_date:
        user_count = User.objects.filter(
            date_joined__date=current_date.date()
        ).count()
        
        user_registration_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'users': user_count
        })
        current_date += timedelta(days=1)
    
    # Top users by booking count
    top_users = User.objects.annotate(
        booking_count=Count('booking'),
        total_spent=Sum('booking__amount_paid')
    ).filter(booking_count__gt=0).order_by('-total_spent')[:10]
    
    # User engagement metrics
    total_users = User.objects.count()
    active_users_30d = User.objects.filter(
        booking__booked_at__gte=start_date
    ).distinct().count()
    active_users_7d = User.objects.filter(
        booking__booked_at__gte=end_date - timedelta(days=7)
    ).distinct().count()
    
    context = {
        'user_registration_data': json.dumps(user_registration_data),
        'top_users': top_users,
        'total_users': total_users,
        'active_users_30d': active_users_30d,
        'active_users_7d': active_users_7d,
        'date_range': {
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d')
        }
    }
    
    return render(request, 'movies/user_analytics.html', context)
