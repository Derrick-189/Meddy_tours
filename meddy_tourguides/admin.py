# from django.contrib import admin
# from .models import Destination
# Register your models here.

# admin.site.register([Destination])

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Destination, BlogPost, TeamMember, Testimonial, DiscountedTour, Video, TourPackage, Accommodation, Booking, ContactMessage, NewsletterSubscriber

class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'offer']
    list_editable = ['price', 'offer']
    list_filter = ['offer']
    search_fields = ['name']

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content']

class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position']
    search_fields = ['name', 'position']

class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'position']
    search_fields = ['name', 'position']

class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title', 'description']
    actions = ['generate_missing_thumbnails']

    def generate_missing_thumbnails(self, request, queryset):
        created = 0
        for video in queryset:
            if not video.thumbnail or not video.thumbnail.name:
                if video.generate_thumbnail():
                    video.save(update_fields=["thumbnail"])  # persist
                    created += 1
        self.message_user(request, f"Generated {created} thumbnails.")

    generate_missing_thumbnails.short_description = "Generate thumbnails for selected videos"

class DiscountedTourAdmin(admin.ModelAdmin):
    list_display = ['name', 'original_price', 'discounted_price', 'discount_percentage', 'is_active']
    list_editable = ['original_price', 'discounted_price', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['discount_percentage']

# Register your models with the main admin site
admin.site.register(Destination, DestinationAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(DiscountedTour, DiscountedTourAdmin)
admin.site.register(Video, VideoAdmin)

# Booking domain registrations
@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "package_type", "duration_days", "original_price", "discounted_price", "is_active")
    list_filter = ("package_type", "is_active", "created_at")
    search_fields = ("name", "description")

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ("name", "accommodation_type", "price_per_night", "location", "is_active")
    list_filter = ("accommodation_type", "is_active", "created_at")
    search_fields = ("name", "location", "description")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("booking_reference", "first_name", "last_name", "tour_package", "travel_date", "number_of_persons", "formatted_total", "status", "confirmed_at")
    list_filter = ("status", "travel_date", "created_at", "confirmed_at")
    search_fields = ("first_name", "last_name", "email", "booking_reference")
    readonly_fields = ("booking_reference", "created_at", "updated_at", "confirmed_at")
    actions = ["mark_selected_as_confirmed"]

    @admin.display(description="Total")
    def formatted_total(self, obj):
        try:
            return f"${obj.total_amount:.2f}"
        except Exception:
            return obj.total_amount

    def mark_selected_as_confirmed(self, request, queryset):
        updated = 0
        for booking in queryset:
            if booking.status != 'confirmed':
                booking.status = 'confirmed'
                booking.save()
                updated += 1
        self.message_user(request, f"Marked {updated} booking(s) as confirmed.")
    mark_selected_as_confirmed.short_description = "Mark selected as Confirmed"

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "first_name", "last_name", "email", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("first_name", "last_name", "email", "subject")

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "subscribed_at")
    list_filter = ("is_active", "subscribed_at")

# Create custom admin site for content managers
class ContentManagerAdminSite(admin.AdminSite):
    site_header = 'Meddy Tours Content Management'
    site_title = 'Content Manager Portal'
    index_title = 'Content Management'

content_manager_site = ContentManagerAdminSite(name='content_manager')

# Register limited models for content managers
content_manager_site.register(BlogPost, BlogPostAdmin)
content_manager_site.register(TeamMember, TeamMemberAdmin)
content_manager_site.register(Testimonial, TestimonialAdmin)
content_manager_site.register(DiscountedTour, DiscountedTourAdmin)
content_manager_site.register(Video, VideoAdmin)