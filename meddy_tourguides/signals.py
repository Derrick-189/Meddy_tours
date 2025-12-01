"""
Django Signals for Automatic Image Optimization

This module automatically optimizes images whenever they are uploaded
through Django admin or saved programmatically.

Usage:
    - Add to apps.py: ready() method that imports this module
    - Images will auto-optimize on upload/save
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from PIL import Image
import io
import os
from pathlib import Path

# Import your models (adjust based on your actual models)
try:
    from .models import BlogPost, Destination, Accommodation, DiscountedTour, Video
    MODELS_TO_OPTIMIZE = [BlogPost, Destination, Accommodation, DiscountedTour, Video]
except ImportError:
    MODELS_TO_OPTIMIZE = []

# Configuration
MAX_WIDTH = 1920
MAX_HEIGHT = 1080
JPEG_QUALITY = 85
PNG_QUALITY = 85
ENABLE_AUTO_OPTIMIZE = True  # Set to False to disable auto-optimization


def optimize_image_file(image_field):
    """
    Optimize an image field in place
    
    Args:
        image_field: Django ImageField instance
        
    Returns:
        bool: True if optimized, False if skipped
    """
    if not ENABLE_AUTO_OPTIMIZE:
        return False
    
    if not image_field or not image_field.name:
        return False
    
    try:
        # Get the file
        img_file = image_field.file
        img_file.seek(0)
        
        # Open with PIL
        img = Image.open(img_file)
        
        # Skip very small files
        file_size = img_file.size
        if file_size < 50 * 1024:  # Less than 50KB
            return False
        
        # Convert RGBA to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                rgb_img.paste(img, mask=img.split()[-1])
            else:
                rgb_img.paste(img)
            img = rgb_img
        
        # Resize if too large
        if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
            img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
        
        # Save optimized
        output = io.BytesIO()
        file_ext = os.path.splitext(image_field.name)[1].lower()
        
        if file_ext in ['.jpg', '.jpeg']:
            img.save(output, format='JPEG', quality=JPEG_QUALITY, optimize=True)
        elif file_ext == '.png':
            img.save(output, format='PNG', optimize=True)
        elif file_ext == '.gif':
            img.save(output, format='GIF', optimize=True)
        else:
            return False
        
        output.seek(0)
        
        # Check if we actually saved anything
        new_size = output.tell() + len(output.getvalue())
        original_size = file_size
        
        # Only update if we actually compressed
        if new_size < original_size:
            image_field.save(
                image_field.name,
                ContentFile(output.getvalue()),
                save=False
            )
            compression_ratio = (1 - new_size / original_size) * 100
            print(f"✓ Optimized: {image_field.name} ({compression_ratio:.1f}% saved)")
            return True
        else:
            print(f"→ Skipped: {image_field.name} (already optimized)")
            return False
    
    except Exception as e:
        print(f"✗ Error optimizing {image_field.name}: {str(e)}")
        return False


@receiver(post_save)
def auto_optimize_images(sender, instance, created, **kwargs):
    """
    Automatically optimize images after model save
    
    Handles all image fields in the model
    """
    if sender not in MODELS_TO_OPTIMIZE:
        return
    
    if not ENABLE_AUTO_OPTIMIZE:
        return
    
    # Get all image fields
    image_fields = []
    for field in sender._meta.get_fields():
        # Check for ImageField
        from django.db.models import ImageField
        if isinstance(field, ImageField):
            image_fields.append(field.name)
    
    if not image_fields:
        return
    
    # Optimize each image field
    optimized = False
    for field_name in image_fields:
        field = getattr(instance, field_name, None)
        if field and field.name:
            if optimize_image_file(field):
                optimized = True
    
    # Save if any optimizations were made
    if optimized:
        # Re-save without triggering signals again
        instance.save(update_fields=image_fields)


def register_signals():
    """
    Register signal handlers
    Call this from apps.py ready() method
    """
    if ENABLE_AUTO_OPTIMIZE:
        print("✓ Auto-optimization signals registered")
