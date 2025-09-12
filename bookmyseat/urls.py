from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('users.urls')),
    path('movies/', include('movies.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # This is the new line that serves your static files (video, images, etc.)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)