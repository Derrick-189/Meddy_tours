"""
URL configuration for meddy_tours project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
<<<<<<< HEAD
from django.views.generic import RedirectView
from meddy_tourguides.admin import content_manager_site

# Base URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('content-manager/', content_manager_site.urls),
    path('', include('meddy_tourguides.urls')),  # Include app's URLs
    # Add redirect for .html URLs without the .html extension
    path('videos', RedirectView.as_view(url='/videos.html/', permanent=True)),
]

# Serve media files in development
=======
from meddy_tourguides.admin import content_manager_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('content-manager/', content_manager_site.urls),
    path('', include('meddy_tourguides.urls')),
]

>>>>>>> 6e674a3e4db70d9c170fa53eccbc7b2fa29be6db
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)