# from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
import os
import io
import numpy as np
import imageio.v3 as iio

# Create your models here.
# class Destination:
#     id : int
#     name : str
#     img : str
#     desc : str
#     price : int
#     offer : bool


from django.db import models
from django.contrib.auth.models import User

class Destination(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.IntegerField()
    img = models.FileField(upload_to='pics', validators=[FileExtensionValidator(["jpg","jpeg","png","gif","webp"])])
    offer = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='blog_images/', validators=[FileExtensionValidator(["jpg","jpeg","png","gif","webp"])])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.FileField(upload_to='team_images/', validators=[FileExtensionValidator(["jpg","jpeg","png","gif","webp"])])
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    
    def __str__(self):
        return self.name

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    content = models.TextField()
    image = models.FileField(upload_to='testimonial_images/', validators=[FileExtensionValidator(["jpg","jpeg","png","gif","webp"])])
    
    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.FileField(upload_to='video_thumbs/', blank=True, validators=[FileExtensionValidator(["jpg","jpeg","png","gif","webp"])])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def generate_thumbnail(self, second: float | None = None) -> bool:
        """Generate a thumbnail from the video.
        Tries moviepy if available; otherwise creates a simple placeholder image.
        Returns True if a thumbnail was created and saved.
        """
        # Guard: need a video file and no existing thumbnail
        if not self.video_file or not os.path.exists(self.video_file.path):
            return False
        # Compute default capture time ~ 1s or middle of video
        capture_time = second
        # Try moviepy first
        try:
            from moviepy.editor import VideoFileClip  # type: ignore
            clip = VideoFileClip(self.video_file.path)
            try:
                if capture_time is None:
                    capture_time = min(1.0, clip.duration / 2 if clip.duration else 0.5)
                frame = clip.get_frame(capture_time)
            finally:
                clip.close()
            # frame is a numpy array; write as PNG without Pillow
            buf = io.BytesIO()
            try:
                iio.imwrite(buf, frame, extension=".png")
            except Exception:
                # Ensure uint8 if needed
                f8 = frame
                if getattr(frame, 'dtype', None) != np.uint8:
                    f8 = np.clip(frame, 0, 255).astype(np.uint8)
                iio.imwrite(buf, f8, extension=".png")
            buf.seek(0)
            filename = f"video_thumbs/{slugify(self.title) or 'video'}-{self.pk or 'new'}.png"
            self.thumbnail.save(filename, ContentFile(buf.read()), save=False)
            return True
        except Exception:
            # Fallback: create a simple placeholder thumbnail with title text
            try:
                # Create a simple solid-color placeholder (no text) to avoid Pillow
                placeholder = np.zeros((360, 640, 3), dtype=np.uint8)
                placeholder[:, :] = (20, 20, 20)
                buf = io.BytesIO()
                iio.imwrite(buf, placeholder, extension=".png")
                buf.seek(0)
                filename = f"video_thumbs/{slugify(self.title) or 'video'}-{self.pk or 'new'}-ph.png"
                self.thumbnail.save(filename, ContentFile(buf.read()), save=False)
                return True
            except Exception:
                return False

    def save(self, *args, **kwargs):
        # First save to get a primary key if new
        creating = self.pk is None
        super().save(*args, **kwargs)
        # If thumbnail missing, try to generate it
        if (creating or not self.thumbnail) and self.video_file and (not self.thumbnail or not os.path.exists(self.thumbnail.path)):
            if self.generate_thumbnail():
                super().save(update_fields=["thumbnail"])  # persist generated thumbnail

class DiscountedTour(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    original_price = models.IntegerField()
    discounted_price = models.IntegerField()
    image = models.FileField(upload_to='discounted_tours/', validators=[FileExtensionValidator(["jpg","jpeg","png","gif","webp"])])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def clean(self):
        # Ensure prices are present and valid when provided
        if self.original_price is not None and self.original_price < 0:
            raise ValidationError({"original_price": "Original price cannot be negative."})
        if self.discounted_price is not None and self.discounted_price < 0:
            raise ValidationError({"discounted_price": "Discounted price cannot be negative."})
        if (
            self.original_price is not None and
            self.discounted_price is not None and
            self.discounted_price > self.original_price
        ):
            raise ValidationError({"discounted_price": "Discounted price cannot exceed original price."})
    
    def discount_percentage(self):
        """Calculate discount percentage"""
        # During admin "add", field values are None, so guard comparisons.
        if self.original_price is None or self.discounted_price is None:
            return 0
        if self.original_price <= 0:
            return 0
        try:
            percentage = int(((self.original_price - self.discounted_price) / self.original_price) * 100)
        except Exception:
            return 0
        # Clamp between 0 and 100 for safety
        return max(0, min(100, percentage))

# === Booking domain models ===

class TourPackage(models.Model):
    PACKAGE_TYPES = [
        ('luxury', 'Luxury'),
        ('mid_range', 'Mid-Range'),
        ('budget', 'Budget'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES)
    duration_days = models.PositiveIntegerField(default=1)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.FileField(upload_to='tour_packages/', validators=[FileExtensionValidator(["jpg","jpeg","png","gif","webp"])])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Accommodation(models.Model):
    ACCOMMODATION_TYPES = [
        ('luxury', 'Luxury'),
        ('mid_range', 'Mid-Range'),
        ('budget', 'Budget'),
    ]

    name = models.CharField(max_length=200)
    accommodation_type = models.CharField(max_length=20, choices=ACCOMMODATION_TYPES)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.FileField(upload_to='accommodations/', validators=[FileExtensionValidator(["jpg","jpeg","png","gif","webp"])])
    location = models.CharField(max_length=200)
    amenities = models.TextField(help_text="Comma-separated list of amenities")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_accommodation_type_display()}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    # Customer Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)

    # Booking Details
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.SET_NULL, null=True, blank=True)
    travel_date = models.DateField()
    number_of_persons = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True, null=True)

    # Metadata
    booking_reference = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Booking #{self.booking_reference} - {self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Compute reference & total
        if not self.booking_reference:
            self.booking_reference = self.generate_booking_reference()
        tour_cost = (self.tour_package.discounted_price or self.tour_package.original_price) if self.tour_package else 0
        acc_cost = self.accommodation.price_per_night if self.accommodation else 0
        self.total_amount = (tour_cost + acc_cost) * self.number_of_persons

        # Auto-set confirmed_at when status becomes confirmed
        just_confirmed = False
        try:
            old_status = None
            if self.pk:
                old_status = Booking.objects.only('status').get(pk=self.pk).status
            if self.status == 'confirmed' and not self.confirmed_at:
                from django.utils import timezone
                self.confirmed_at = timezone.now()
                # treat as newly confirmed if previous status wasn't confirmed
                if old_status != 'confirmed':
                    just_confirmed = True
            # If reverted from confirmed, keep confirmed_at (audit), so do not clear it
        except Exception:
            pass

        super().save(*args, **kwargs)

        # Send confirmation email only when newly confirmed
        if just_confirmed:
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                send_mail(
                    subject=f"Your booking {self.booking_reference} is confirmed",
                    message=(
                        f"Hello {self.first_name},\n\n"
                        f"Your booking has been confirmed.\n"
                        f"Reference: {self.booking_reference}\n"
                        f"Tour: {self.tour_package}\n"
                        f"Travel date: {self.travel_date}\n"
                        f"Persons: {self.number_of_persons}\n"
                        f"Total: ${self.total_amount}\n\n"
                        f"Thank you for choosing Meddy Tours!"
                    ),
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                    recipient_list=[self.email],
                    fail_silently=True,
                )
            except Exception:
                pass

    def generate_booking_reference(self):
        import random, string
        return 'BK' + ''.join(random.choices(string.digits, k=8))

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.first_name} {self.last_name}"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email