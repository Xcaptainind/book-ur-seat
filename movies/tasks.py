from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from .models import SeatReservation, Seat, Booking
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_booking_confirmation_email(booking_id):
    """Send booking confirmation email to user"""
    try:
        booking = Booking.objects.get(id=booking_id)
        if not booking.email_sent:
            subject = f'Booking Confirmation - {booking.movie.name}'
            
            context = {
                'booking': booking,
                'user': booking.user,
                'movie': booking.movie,
                'theater': booking.theater,
                'seat': booking.seat,
            }
            
            html_message = render_to_string('movies/emails/booking_confirmation.html', context)
            plain_message = render_to_string('movies/emails/booking_confirmation.txt', context)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[booking.user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            booking.email_sent = True
            booking.save()
            logger.info(f'Booking confirmation email sent to {booking.user.email}')
            
    except Exception as e:
        logger.error(f'Error sending booking confirmation email: {str(e)}')


@shared_task
def cleanup_expired_reservations():
    """Clean up expired seat reservations and release seats"""
    try:
        expired_reservations = SeatReservation.objects.filter(
            expires_at__lt=timezone.now(),
            is_active=True
        )
        
        for reservation in expired_reservations:
            # Release the seat
            seat = reservation.seat
            seat.status = 'available'
            seat.reserved_until = None
            seat.save()
            
            # Mark reservation as inactive
            reservation.is_active = False
            reservation.save()
            
            logger.info(f'Released expired reservation for seat {seat.seat_number}')
            
        logger.info(f'Cleaned up {expired_reservations.count()} expired reservations')
        
    except Exception as e:
        logger.error(f'Error cleaning up expired reservations: {str(e)}')


@shared_task
def send_reminder_emails():
    """Send reminder emails for upcoming shows"""
    try:
        # Find bookings for shows happening in the next 2 hours
        reminder_time = timezone.now() + timezone.timedelta(hours=2)
        
        upcoming_bookings = Booking.objects.filter(
            theater__time__lte=reminder_time,
            theater__time__gt=timezone.now(),
            payment_status='completed'
        )
        
        for booking in upcoming_bookings:
            subject = f'Reminder: {booking.movie.name} starts in 2 hours'
            
            context = {
                'booking': booking,
                'user': booking.user,
                'movie': booking.movie,
                'theater': booking.theater,
                'seat': booking.seat,
            }
            
            html_message = render_to_string('movies/emails/show_reminder.html', context)
            plain_message = render_to_string('movies/emails/show_reminder.txt', context)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[booking.user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f'Reminder email sent to {booking.user.email}')
            
    except Exception as e:
        logger.error(f'Error sending reminder emails: {str(e)}')
