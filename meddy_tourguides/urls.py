from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('destination.html', views.destination, name='destination'),
    path('discount.html', views.discount, name='discount'),
    path('about.html', views.about, name='about'),
    path('blog.html', views.blog, name='blog'),
    path('contact.html', views.contact, name='contact'),
    path('booking.html', views.booking, name='booking'),
]
