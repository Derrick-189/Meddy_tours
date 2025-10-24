from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import *
from .forms import *

def home(request):
    destinations = Destination.objects.filter(is_active=True)[:6]
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    team_members = TeamMember.objects.filter(is_active=True)[:3]
    discounted_tours = TourPackage.objects.filter(
        is_active=True, 
        discount_percentage__gt=0
    )[:3]
    
    context = {
        'dests': destinations,
        'testimonials': testimonials,
        'team_members': team_members,
        'discounted_tours': discounted_tours,
    }
    return render(request, 'index.html', context)

class DestinationListView(ListView):
    model = Destination
    template_name = 'destination.html'
    context_object_name = 'destinations'
    
    def get_queryset(self):
        return Destination.objects.filter(is_active=True)

class TourPackageListView(ListView):
    model = TourPackage
    template_name = 'packages.html'
    context_object_name = 'packages'
    
    def get_queryset(self):
        return TourPackage.objects.filter(is_active=True)

class DiscountedToursView(ListView):
    model = TourPackage
    template_name = 'discount.html'
    context_object_name = 'discounted_tours'
    
    def get_queryset(self):
        return TourPackage.objects.filter(
            is_active=True, 
            discount_percentage__gt=0
        )

class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking.html'
    success_url = reverse_lazy('booking_success')
    
    def form_valid(self, form):
        messages.success(self.request, 'Your booking has been submitted successfully! We will contact you soon.')
        return super().form_valid(form)

def booking_success(request):
    return render(request, 'booking_success.html')

class ContactView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = reverse_lazy('contact_success')
    
    def form_valid(self, form):
        messages.success(self.request, 'Your message has been sent successfully! We will get back to you soon.')
        return super().form_valid(form)

def contact_success(request):
    return render(request, 'contact_success.html')

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Successfully subscribed to our newsletter!'})
        else:
            return JsonResponse({'success': False, 'message': 'This email is already subscribed.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

# API views for AJAX calls
def get_accommodations_by_type(request):
    accommodation_type = request.GET.get('type')
    accommodations = Accommodation.objects.filter(
        accommodation_type=accommodation_type, 
        is_active=True
    ).values('id', 'name', 'price_per_night')
    return JsonResponse(list(accommodations), safe=False)

def calculate_booking_total(request):
    tour_package_id = request.GET.get('tour_package')
    accommodation_id = request.GET.get('accommodation')
    persons = int(request.GET.get('persons', 1))
    
    total = 0
    
    if tour_package_id:
        tour_package = get_object_or_404(TourPackage, id=tour_package_id)
        tour_cost = tour_package.discounted_price or tour_package.original_price
        total += tour_cost * persons
    
    if accommodation_id:
        accommodation = get_object_or_404(Accommodation, id=accommodation_id)
        total += accommodation.price_per_night * persons
    
    return JsonResponse({'total_amount': float(total)})