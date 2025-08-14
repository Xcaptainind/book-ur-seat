from django.urls import path
from . import views
from . import payment_views
from . import admin_dashboard

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('<int:movie_id>/theaters', views.theater_list, name='theater_list'),
    path('theater/<int:theater_id>/seats/book/', views.book_seats, name='book_seats'),
    
    # Payment URLs
    path('theater/<int:theater_id>/payment/', payment_views.payment_page, name='payment_page'),
    path('theater/<int:theater_id>/stripe-payment/', payment_views.stripe_payment, name='stripe_payment'),
    path('theater/<int:theater_id>/razorpay-payment/', payment_views.razorpay_payment, name='razorpay_payment'),
    path('payment/success/', payment_views.payment_success, name='payment_success'),
    path('payment/failure/', payment_views.payment_failure, name='payment_failure'),
    path('webhook/stripe/', payment_views.stripe_webhook, name='stripe_webhook'),
    path('webhook/razorpay/', payment_views.razorpay_webhook, name='razorpay_webhook'),
    
    # Admin Dashboard URLs
    path('admin/dashboard/', admin_dashboard.admin_dashboard, name='admin_dashboard'),
    path('admin/revenue-report/', admin_dashboard.revenue_report, name='revenue_report'),
    path('admin/user-analytics/', admin_dashboard.user_analytics, name='user_analytics'),
]