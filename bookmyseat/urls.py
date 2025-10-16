# bookmyseat/urls.py

from django.contrib import admin
from django.urls import path, include
from movies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', views.home, name='home'),
    path('register/', include('users.urls')),
    path('login/', include('users.urls')),
    path('profile/', include('users.urls')),
    path('reset-password/', include('users.urls')),
    path('logout/', include('users.urls')),
    path('password-reset/', include('django.contrib.auth.urls')),
    path('movies/', include('movies.urls_movies')),
    path('events/', include('movies.urls_events')),
]