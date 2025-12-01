from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about.html', views.about, name='about'),
    path('blog.html', views.blog, name='blog'),
    path('destination.html', views.destination, name='destination'),  # Fixed function name
    path('contact', views.contact, name='contact'),
    path('discount.html', views.discount, name='discount'),
    # Booking endpoints
    path('booking.html', views.booking, name='booking'),
    path('booking/success/', views.booking_success, name='booking_success'),
    # API endpoints used by booking JS
    path('api/accommodations/', views.get_accommodations_by_type, name='get_accommodations'),
    path('api/calculate-total/', views.calculate_booking_total, name='calculate_total'),
    # Newsletter subscribe
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    # Videos page - handle both with and without .html extension
    path('videos.html/', views.videos, name='videos'),
    path('videos/', views.videos, name='videos'),
    path('packages/', views.packages, name='packages'),
    path('packages.html', views.packages),
    path('packages', views.packages),
    # New routes for attached templates
    path('service', views.services, name='services'),
    path('service.html', views.services),
    path('testimonial', views.testimonial, name='testimonial'),
    path('testimonial.html', views.testimonial),
    path('accomodation', views.accomodation, name='accomodation'),
    path('accomodation.html', views.accomodation),
]
# urlpatterns = [
#     path('', views.index, name='index'),
#     path('destination.html', views.destination, name='destination'),
#     path('discount.html', views.discount, name='discount'),
#     path('about.html', views.about, name='about'),
#     path('blog.html', views.blog, name='blog'),
#     path('contact.html', views.contact, name='contact'),
#     # path('booking.html', views.booking, name='booking'),
# ]
