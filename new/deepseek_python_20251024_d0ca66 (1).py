from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active',)

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'package_type', 'duration_days', 'original_price', 
                   'discounted_price', 'discount_percentage', 'is_active')
    list_filter = ('package_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('destinations',)
    
    def save_model(self, request, obj, form, change):
        if obj.discounted_price and obj.original_price:
            discount = ((obj.original_price - obj.discounted_price) / obj.original_price) * 100
            obj.discount_percentage = round(discount)
        super().save_model(request, obj, form, change)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'position')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'rating', 'is_active', 'created_at')
    list_filter = ('rating', 'is_active', 'created_at')
    search_fields = ('name', 'content')

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('name', 'accommodation_type', 'price_per_night', 'location', 'is_active')
    list_filter = ('accommodation_type', 'is_active', 'created_at')
    search_fields = ('name', 'location', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'customer_name', 'tour_package', 'travel_date', 
                   'number_of_persons', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'travel_date', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'booking_reference')
    readonly_fields = ('booking_reference', 'created_at', 'updated_at')
    list_editable = ('status',)
    
    def customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    customer_name.short_description = 'Customer'

    fieldsets = (
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Booking Details', {
            'fields': ('tour_package', 'accommodation', 'travel_date', 'number_of_persons', 'special_requests')
        }),
        ('Booking Information', {
            'fields': ('booking_reference', 'status', 'total_amount', 'created_at', 'updated_at')
        }),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'customer_name', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'subject')
    readonly_fields = ('first_name', 'last_name', 'email', 'subject', 'message', 'created_at')
    list_editable = ('status',)
    
    def customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    customer_name.short_description = 'Customer'

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    list_editable = ('is_active',)

# Custom Admin Site Configuration
admin.site.site_header = "Meddy Tours Administration"
admin.site.site_title = "Meddy Tours Admin"
admin.site.index_title = "Welcome to Meddy Tours Admin Panel"