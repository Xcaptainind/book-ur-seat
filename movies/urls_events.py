from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.list_view, name='list'),
    path('<slug:event_slug>/', views.event_detail, name='event_detail'),
    path('<slug:event_slug>/book/', views.book_event, name='book_event'),
]