from django import forms
from .models import Movie, Theater, Seat


class MovieFilterForm(forms.Form):
    genre = forms.ChoiceField(
        choices=[('', 'All Genres')] + Movie.GENRE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    language = forms.ChoiceField(
        choices=[('', 'All Languages')] + Movie.LANGUAGE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    search = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search movies...'
        })
    )


class SeatSelectionForm(forms.Form):
    selected_seats = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    def __init__(self, available_seats, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selected_seats'].choices = [
            (seat.id, f"{seat.seat_number} - ₹{seat.price or seat.theater.price_per_seat}")
            for seat in available_seats
        ]


class PaymentForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('stripe', 'Credit/Debit Card (Stripe)'),
        ('razorpay', 'UPI/Net Banking (Razorpay)'),
    ]
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True
    )
    
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
