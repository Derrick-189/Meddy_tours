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
    
    @property
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