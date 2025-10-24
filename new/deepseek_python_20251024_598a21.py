from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('destinations/', views.DestinationListView.as_view(), name='destination'),
    path('packages/', views.TourPackageListView.as_view(), name='packages'),
    path('discount/', views.DiscountedToursView.as_view(), name='discount'),
    path('booking/', views.BookingCreateView.as_view(), name='booking'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    
    # API endpoints
    path('api/accommodations/', views.get_accommodations_by_type, name='get_accommodations'),
    path('api/calculate-total/', views.calculate_booking_total, name='calculate_total'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)