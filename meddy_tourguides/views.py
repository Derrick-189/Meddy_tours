from django.shortcuts import render
from .models import Destination
# Create your views here.
def index(request):

    dest1 = Destination()
    dest1.name = 'Santorini, Greece'
    dest1.desc = 'Santorini is a beautiful island in Greece known for its stunning sunsets, white-washed buildings, and crystal-clear waters.'
    dest1.price = 590
    dest1.img = 'images/01-greece.jpg'
    dest1.offer = False

    dest2 = Destination()
    dest2.name = 'Rome, Italy'
    dest2.desc = 'Rome, the capital of Italy, is a city rich in history and culture, famous for its ancient ruins, art, and architecture.'
    dest2.price = 390
    dest2.img = 'images/02-rome.jpg'
    dest2.offer = False

    dest3 = Destination()
    dest3.name = 'Mount Fuji, Japan'
    dest3.desc = 'Mount Fuji is Japan\'s highest peak and an iconic symbol of the country, offering breathtaking views and hiking opportunities.'
    dest3.price = 390
    dest3.img = 'images/03-japan.jpg'
    dest3.offer = False

    dest4 = Destination()
    dest4.name = 'Camels, Dubai'
    dest4.desc = 'Dubai is known for its modern architecture, luxury shopping, and vibrant nightlife, with the iconic Burj Khalifa dominating the skyline.'
    dest4.price = 320
    dest4.img = 'images/04-dubai.jpg'
    dest4.offer = True

    dest5 = Destination()
    dest4.name = 'Elizabeth Tower, London'
    dest5.desc = 'The Elizabeth Tower, commonly known as Big Ben, is a famous clock tower in London, symbolizing the city\'s rich history and culture.'
    dest5.price = 290
    dest5.img = 'images/05-london.jpg'
    dest5.offer = True

    dest6 = Destination()
    dest6.name = 'Opera House, Australia'
    dest6.desc = 'The Sydney Opera House is an iconic architectural masterpiece in Australia, known for its unique design and cultural significance.'
    dest6.price = 390
    dest6.img = 'images/06-australia.jpg'
    dest6.offer = False
    
    #return render(request, 'index.html', {'dest1': dest1, 'dest2': dest2, 'dest3': dest3, 'dest4': dest4, 'dest5': dest5, 'dest6': dest6})
    # # The above code defines a view function that creates several destination objects and renders them in the 'index.html' template.
    # # Each destination has a name, description, price, and image associated with it.
    # to return every object at once, we can use a list or dictionary to store them and pass it to the template.
    dests = [dest1, dest2, dest3, dest4, dest5, dest6]
    return render(request, 'index.html', {'dests': dests})
def destination(request):
    return render(request, 'destination.html') 
def discount(request):
    return render(request, 'discount.html') 
def about(request):
    return render(request, 'about.html')
def blog(request):
    return render(request, 'blog.html')
def contact(request):
    return render(request, 'contact.html')
def booking(request):
    return render(request, 'booking.html')     

