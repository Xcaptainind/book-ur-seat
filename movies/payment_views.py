import stripe
# import razorpay  # Commented out for now - will add later
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from .models import Seat, Theater, Booking, SeatReservation
from .forms import PaymentForm
from .tasks import send_booking_confirmation_email
import json
import logging

logger = logging.getLogger(__name__)

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Configure Razorpay (commented out for now)
# razorpay_client = razorpay.Client(
#     auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
# )


@login_required
def payment_page(request, theater_id):
    """Display payment page with selected seats"""
    theater = get_object_or_404(Theater, id=theater_id)
    selected_seat_ids = request.session.get('selected_seats', [])
    
    if not selected_seat_ids:
        messages.error(request, 'No seats selected for booking.')
        return redirect('theater_list')
    
    selected_seats = Seat.objects.filter(id__in=selected_seat_ids, theater=theater)
    total_amount = sum(seat.price or theater.price_per_seat for seat in selected_seats)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            
            # Store payment details in session
            request.session['payment_details'] = {
                'payment_method': payment_method,
                'email': email,
                'phone': phone,
                'total_amount': float(total_amount)
            }
            
            if payment_method == 'stripe':
                return redirect('stripe_payment', theater_id=theater_id)
            # elif payment_method == 'razorpay': # Removed razorpay payment option
            #     return redirect('razorpay_payment', theater_id=theater_id)
    else:
        form = PaymentForm()
    
    context = {
        'theater': theater,
        'selected_seats': selected_seats,
        'total_amount': total_amount,
        'form': form,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'movies/payment_page.html', context)


@login_required
def stripe_payment(request, theater_id):
    """Handle Stripe payment"""
    theater = get_object_or_404(Theater, id=theater_id)
    payment_details = request.session.get('payment_details', {})
    
    if not payment_details:
        messages.error(request, 'Payment details not found.')
        return redirect('payment_page', theater_id=theater_id)
    
    try:
        # Create Stripe payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(payment_details['total_amount'] * 100),  # Convert to cents
            currency='inr',
            metadata={
                'theater_id': theater_id,
                'user_id': request.user.id,
            }
        )
        
        context = {
            'theater': theater,
            'client_secret': intent.client_secret,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            'amount': payment_details['total_amount'],
        }
        return render(request, 'movies/stripe_payment.html', context)
        
    except Exception as e:
        logger.error(f'Stripe payment intent creation failed: {str(e)}')
        messages.error(request, 'Payment initialization failed. Please try again.')
        return redirect('payment_page', theater_id=theater_id)


@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhook for payment confirmation"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment(payment_intent, 'stripe')
    
    return JsonResponse({'status': 'success'})


# @login_required
# def razorpay_payment(request, theater_id):
#     """Handle Razorpay payment"""
#     theater = get_object_or_404(Theater, id=theater_id)
#     payment_details = request.session.get('payment_details', {})
    
#     if not payment_details:
#         messages.error(request, 'Payment details not found.')
#         return redirect('payment_page', theater_id=theater_id)
    
#     # Create Razorpay order
#     try:
#         order_data = {
#             'amount': int(payment_details['total_amount'] * 100),  # Convert to paise
#             'currency': 'INR',
#             'receipt': f'order_{theater_id}_{request.user.id}',
#             'notes': {
#                 'theater_id': str(theater_id),
#                 'user_id': str(request.user.id),
#             }
#         }
        
#         razorpay_order = razorpay_client.order.create(data=order_data)
        
#         context = {
#             'theater': theater,
#             'razorpay_order_id': razorpay_order['id'],
#             'razorpay_key_id': settings.RAZORPAY_KEY_ID,
#             'amount': payment_details['total_amount'],
#             'user_email': payment_details['email'],
#             'user_phone': payment_details['phone'],
#         }
#         return render(request, 'movies/razorpay_payment.html', context)
        
#     except Exception as e:
#         logger.error(f'Razorpay order creation failed: {str(e)}')
#         messages.error(request, 'Payment initialization failed. Please try again.')
#         return redirect('payment_page', theater_id=theater_id)


# @csrf_exempt
# def razorpay_webhook(request):
#     """Handle Razorpay webhook for payment confirmation"""
#     try:
#         # Verify webhook signature
#         webhook_signature = request.META.get('HTTP_X_RAZORPAY_SIGNATURE')
#         webhook_body = request.body
        
#         razorpay_client.utility.verify_webhook_signature(
#             webhook_body, webhook_signature, settings.RAZORPAY_WEBHOOK_SECRET
#         )
        
#         # Parse webhook data
#         webhook_data = json.loads(webhook_body)
        
#         if webhook_data['event'] == 'payment.captured':
#             payment_data = webhook_data['payload']['payment']['entity']
#             handle_successful_payment(payment_data, 'razorpay')
        
#         return JsonResponse({'status': 'success'})
        
#     except Exception as e:
#         logger.error(f'Razorpay webhook verification failed: {str(e)}')
#         return JsonResponse({'error': 'Webhook verification failed'}, status=400)


def handle_successful_payment(payment_data, payment_method):
    """Handle successful payment and create booking"""
    try:
        if payment_method == 'stripe':
            theater_id = payment_data['metadata']['theater_id']
            user_id = payment_data['metadata']['user_id']
            transaction_id = payment_data['id']
            amount = payment_data['amount'] / 100  # Convert from cents
        # else:  # Razorpay # Removed razorpay handling
        #     theater_id = payment_data['notes']['theater_id'] # Removed razorpay handling
        #     user_id = payment_data['notes']['user_id'] # Removed razorpay handling
        #     transaction_id = payment_data['id'] # Removed razorpay handling
        #     amount = payment_data['amount'] / 100  # Convert from paise # Removed razorpay handling
        
        # Create booking for each selected seat
        selected_seat_ids = SeatReservation.objects.filter(
            user_id=user_id,
            theater_id=theater_id,
            is_active=True
        ).values_list('seat_id', flat=True)
        
        for seat_id in selected_seat_ids:
            seat = Seat.objects.get(id=seat_id)
            
            # Create booking
            booking = Booking.objects.create(
                user_id=user_id,
                seat=seat,
                movie=seat.theater.movie,
                theater=seat.theater,
                payment_status='completed',
                payment_method=payment_method,
                amount_paid=amount,
                transaction_id=transaction_id,
            )
            
            # Update seat status
            seat.status = 'booked'
            seat.save()
            
            # Mark reservation as inactive
            SeatReservation.objects.filter(
                user_id=user_id,
                seat_id=seat_id,
                theater_id=theater_id
            ).update(is_active=False)
            
            # Send confirmation email
            send_booking_confirmation_email.delay(booking.id)
        
        logger.info(f'Successfully created booking for user {user_id} with {payment_method}')
        
    except Exception as e:
        logger.error(f'Error handling successful payment: {str(e)}')


@login_required
def payment_success(request):
    """Display payment success page"""
    messages.success(request, 'Payment successful! Your booking has been confirmed.')
    return render(request, 'movies/payment_success.html')


@login_required
def payment_failure(request):
    """Display payment failure page"""
    messages.error(request, 'Payment failed. Please try again.')
    return render(request, 'movies/payment_failure.html')
