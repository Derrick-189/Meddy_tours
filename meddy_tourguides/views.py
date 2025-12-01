from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
<<<<<<< HEAD
from .models import Destination, BlogPost, TeamMember, Testimonial, DiscountedTour, Video, Image, Booking, Accommodation, TourPackage, NewsletterSubscriber
=======
from .models import Destination, BlogPost, TeamMember, Testimonial, DiscountedTour, Video, Booking, Accommodation, TourPackage, NewsletterSubscriber
>>>>>>> 6e674a3e4db70d9c170fa53eccbc7b2fa29be6db
from .forms import BookingForm

def index(request):
    dests = Destination.objects.all()
    testimonials = Testimonial.objects.all()[:3]
    blog_posts = BlogPost.objects.all().order_by('-created_at')[:2]
    
    context = {
        'dests': dests,
        'testimonials': testimonials,
        'blog_posts': blog_posts,
    }
    return render(request, 'index.html', context)

def about(request):
    team_members = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()
    
    context = {
        'team_members': team_members,
        'testimonials': testimonials,
    }
    return render(request, 'about.html', context)

def blog(request):
    blog_posts = BlogPost.objects.all().order_by('-created_at')
    
    context = {
        'blog_posts': blog_posts,
    }
    return render(request, 'blog.html', context)

def destination(request):
    destinations = Destination.objects.all()
    return render(request, 'destination.html', {'destinations': destinations})

def contact(request):
    return render(request, 'contact.html')

def discount(request):
    discounted_tours = DiscountedTour.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'discount.html', {'discounted_tours': discounted_tours})

def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            return redirect(f"/booking/success/?ref={booking.booking_reference}")
    else:
        form = BookingForm()
    return render(request, 'booking.html', { 'form': form })

def booking_success(request):
    ref = request.GET.get('ref')
    booking = None
    if ref:
        booking = Booking.objects.filter(booking_reference=ref).first()
    return render(request, 'booking_success.html', { 'booking': booking })

# --- API endpoints used by the provided JS ---
def get_accommodations_by_type(request):
    acc_type = request.GET.get('type')
    qs = Accommodation.objects.filter(is_active=True)
    if acc_type:
        qs = qs.filter(accommodation_type=acc_type)
    data = [
        {
            'id': a.id,
            'name': a.name,
            'price_per_night': float(a.price_per_night),
        } for a in qs
    ]
    return JsonResponse(data, safe=False)

def calculate_booking_total(request):
    try:
        tour_id = request.GET.get('tour_package')
        acc_id = request.GET.get('accommodation')
        persons = int(request.GET.get('persons') or 1)
        total = 0
        if tour_id:
            tour = TourPackage.objects.get(id=tour_id)
            tour_cost = tour.discounted_price or tour.original_price
            total += float(tour_cost)
        if acc_id:
            acc = Accommodation.objects.get(id=acc_id)
            total += float(acc.price_per_night)
        total *= max(1, persons)
        return JsonResponse({'total_amount': round(total, 2)})
    except Exception:
        return JsonResponse({'total_amount': 0})

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return JsonResponse({'success': False, 'message': 'Email is required.'})
        obj, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if not created:
            obj.is_active = True
            obj.save(update_fields=['is_active'])
        return JsonResponse({'success': True, 'message': 'Subscribed successfully!'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)

def videos(request):
    videos = Video.objects.all().order_by('-created_at')
<<<<<<< HEAD
    images = Image.objects.all().order_by('-created_at')
    
    # Get unique categories for filtering
    video_categories = Video.objects.exclude(category__isnull=True).exclude(category='').values_list('category', flat=True).distinct()
    image_categories = Image.objects.exclude(category__isnull=True).exclude(category='').values_list('category', flat=True).distinct()
    
    # Combine and deduplicate categories
    all_categories = sorted(list(set(list(video_categories) + list(image_categories))))
    
    context = {
        'videos': videos,
        'images': images,
        'all_categories': all_categories,
    }
    return render(request, 'videos.html', context)
=======
    return render(request, 'videos.html', { 'videos': videos })
>>>>>>> 6e674a3e4db70d9c170fa53eccbc7b2fa29be6db

# New: Packages page using ported styling template
def packages(request):
    return render(request, 'packages.html')

# New: Services page
def services(request):
    return render(request, 'services_site.html')

# New: Testimonial page
def testimonial(request):
    return render(request, 'testimonial_site.html')

# New: Accommodation page
def accomodation(request):
    return render(request, 'accomodation_site.html')


# from django.shortcuts import render
# from .models import Destination
# # Create your views here.
# def index(request):

#     dest1 = Destination()
#     dest1.name = 'Santorini, Greece'
#     dest1.desc = 'Santorini is a beautiful island in Greece known for its stunning sunsets, white-washed buildings, and crystal-clear waters.'
#     dest1.price = 590
#     dest1.img = 'images/01-greece.jpg'
#     dest1.offer = False

#     dest2 = Destination()
#     dest2.name = 'Rome, Italy'
#     dest2.desc = 'Rome, the capital of Italy, is a city rich in history and culture, famous for its ancient ruins, art, and architecture.'
#     dest2.price = 390
#     dest2.img = 'images/02-rome.jpg'
#     dest2.offer = False

#     dest3 = Destination()
#     dest3.name = 'Mount Fuji, Japan'
#     dest3.desc = 'Mount Fuji is Japan\'s highest peak and an iconic symbol of the country, offering breathtaking views and hiking opportunities.'
#     dest3.price = 390
#     dest3.img = 'images/03-japan.jpg'
#     dest3.offer = False

#     dest4 = Destination()
#     dest4.name = 'Camels, Dubai'
#     dest4.desc = 'Dubai is known for its modern architecture, luxury shopping, and vibrant nightlife, with the iconic Burj Khalifa dominating the skyline.'
#     dest4.price = 320
#     dest4.img = 'images/04-dubai.jpg'
#     dest4.offer = True

#     dest5 = Destination()
#     dest4.name = 'Elizabeth Tower, London'
#     dest5.desc = 'The Elizabeth Tower, commonly known as Big Ben, is a famous clock tower in London, symbolizing the city\'s rich history and culture.'
#     dest5.price = 290
#     dest5.img = 'images/05-london.jpg'
#     dest5.offer = True

#     dest6 = Destination()
#     dest6.name = 'Opera House, Australia'
#     dest6.desc = 'The Sydney Opera House is an iconic architectural masterpiece in Australia, known for its unique design and cultural significance.'
#     dest6.price = 390
#     dest6.img = 'images/06-australia.jpg'
#     dest6.offer = False
    
#     #return render(request, 'index.html', {'dest1': dest1, 'dest2': dest2, 'dest3': dest3, 'dest4': dest4, 'dest5': dest5, 'dest6': dest6})
#     # # The above code defines a view function that creates several destination objects and renders them in the 'index.html' template.
#     # # Each destination has a name, description, price, and image associated with it.
#     # to return every object at once, we can use a list or dictionary to store them and pass it to the template.
#     dests = [dest1, dest2, dest3, dest4, dest5, dest6]
#     return render(request, 'index.html', {'dests': dests})
# def destination(request):
#     return render(request, 'destination.html') 
# def discount(request):
#     return render(request, 'discount.html') 
# def about(request):
#     return render(request, 'about.html')
# def blog(request):
#     return render(request, 'blog.html')
# def contact(request):
#     return render(request, 'contact.html')
# def booking(request):
#     return render(request, 'booking.html')



