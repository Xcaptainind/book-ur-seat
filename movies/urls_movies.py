from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.list_view, name='list'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_id>/theaters/', views.theater_list, name='theater_list'),
    path('theater/<int:theater_id>/seats/book/', views.book_seats, name='book_seats'),
]