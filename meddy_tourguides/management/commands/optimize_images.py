"""
Management command to optimize all images in a model
Usage: python manage.py optimize_images --model=BlogPost
"""

from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from PIL import Image
import io
import os
from pathlib import Path

MAX_WIDTH = 1920
MAX_HEIGHT = 1080
JPEG_QUALITY = 85


class Command(BaseCommand):
    help = 'Optimize all images in specified model(s)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            help='Model name to optimize (e.g., BlogPost, Destination)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Optimize images in all models',
        )
        parser.add_argument(
            '--static',
            action='store_true',
            help='Optimize images in static/assets directories',
        )

    def optimize_image_object(self, instance, field_name):
        """Optimize a single image field"""
        try:
            image_field = getattr(instance, field_name, None)
            if not image_field or not image_field.name:
                return False, "No image"
            
            # Get file size
            file_path = image_field.path
            original_size = os.path.getsize(file_path)
            
            # Skip small files
            if original_size < 50 * 1024:
                return False, "Too small"
            
            # Open and optimize
            img = Image.open(file_path)
            
            # Convert RGBA to RGB
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    rgb_img.paste(img, mask=img.split()[-1])
                else:
                    rgb_img.paste(img)
                img = rgb_img
            
            # Resize if needed
            if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
                img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
            
            # Save
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext in ['.jpg', '.jpeg']:
                img.save(file_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
            elif file_ext == '.png':
                img.save(file_path, 'PNG', optimize=True)
            else:
                return False, "Unsupported format"
            
            # Check compression
            new_size = os.path.getsize(file_path)
            if new_size < original_size:
                compression = (1 - new_size / original_size) * 100
                return True, f"{compression:.1f}% saved"
            else:
                return False, "Already optimized"
        
        except Exception as e:
            return False, str(e)

    def handle(self, *args, **options):
        from django.apps import apps
        
        if options['static']:
            self.optimize_static_images()
            return
        
        models_to_process = []
        
        if options['model']:
            try:
                app_label, model_name = options['model'].split('.')
            except ValueError:
                app_label = 'meddy_tourguides'
                model_name = options['model']
            
            try:
                model = apps.get_model(app_label, model_name)
                models_to_process = [model]
            except LookupError:
                raise CommandError(f'Model {options["model"]} not found')
        
        elif options['all']:
            app = apps.get_app_config('meddy_tourguides')
            models_to_process = app.get_models()
        
        else:
            raise CommandError('Please specify --model or --all')
        
        total_optimized = 0
        total_skipped = 0
        total_saved = 0
        
        for model in models_to_process:
            self.stdout.write(f"\n📊 Processing {model.__name__}...")
            
            # Get image fields
            image_fields = []
            for field in model._meta.get_fields():
                from django.db.models import ImageField
                if isinstance(field, ImageField):
                    image_fields.append(field.name)
            
            if not image_fields:
                self.stdout.write(f"  No image fields found")
                continue
            
            # Process each instance
            for instance in model.objects.all():
                for field_name in image_fields:
                    success, message = self.optimize_image_object(instance, field_name)
                    
                    if success:
                        total_optimized += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"  ✓ {getattr(instance, field_name).name}: {message}")
                        )
                    else:
                        total_skipped += 1
        
        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(self.style.SUCCESS(f"✓ Optimized: {total_optimized}"))
        self.stdout.write(f"→ Skipped: {total_skipped}")

    def optimize_static_images(self):
        """Optimize images in static directories"""
        base_paths = [
            '/home/slade/Meddy_Tours/assets/images',
            '/home/slade/Meddy_Tours/static/images',
        ]
        
        total = 0
        for base_path in base_paths:
            if not os.path.exists(base_path):
                continue
            
            for filename in os.listdir(base_path):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    filepath = os.path.join(base_path, filename)
                    try:
                        img = Image.open(filepath)
                        
                        if img.mode in ('RGBA', 'LA', 'P'):
                            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                            if img.mode == 'RGBA':
                                rgb_img.paste(img, mask=img.split()[-1])
                            else:
                                rgb_img.paste(img)
                            img = rgb_img
                        
                        if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
                            img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
                        
                        ext = filename.split('.')[-1].lower()
                        if ext in ['jpg', 'jpeg']:
                            img.save(filepath, 'JPEG', quality=JPEG_QUALITY, optimize=True)
                        elif ext == 'png':
                            img.save(filepath, 'PNG', optimize=True)
                        
                        total += 1
                        self.stdout.write(self.style.SUCCESS(f"✓ {filename}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"✗ {filename}: {str(e)}"))
        
        self.stdout.write(f"\nOptimized {total} images")
