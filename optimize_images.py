#!/usr/bin/env python3
"""
Image Optimization Script for Meddy Tours
Compresses all images in assets/images directory to optimize website loading
"""

import os
import sys
from PIL import Image
import shutil
from pathlib import Path

# Configuration
ASSETS_DIR = '/home/slade/Meddy_Tours/assets/images'
BACKUP_DIR = '/home/slade/Meddy_Tours/assets/images_backup'
MAX_WIDTH = 1920
MAX_HEIGHT = 1080
JPEG_QUALITY = 85
PNG_QUALITY = 85
TARGET_SIZE_KB = 150

def format_size(bytes):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} GB"

def optimize_image(image_path):
    """
    Optimize a single image file
    Returns: (original_size, optimized_size, success)
    """
    try:
        original_size = os.path.getsize(image_path)
        
        # Skip if file is too small to optimize
        if original_size < 50 * 1024:  # Less than 50KB
            return original_size, original_size, True
        
        img = Image.open(image_path)
        
        # Convert RGBA to RGB if necessary (for JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        
        # Calculate new dimensions while maintaining aspect ratio
        img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
        
        # Save optimized image
        file_ext = os.path.splitext(image_path)[1].lower()
        
        if file_ext in ['.jpg', '.jpeg']:
            img.save(image_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
        elif file_ext == '.png':
            img.save(image_path, 'PNG', optimize=True)
        elif file_ext == '.gif':
            img.save(image_path, 'GIF', optimize=True)
        else:
            return original_size, original_size, True
        
        optimized_size = os.path.getsize(image_path)
        compression_ratio = (1 - optimized_size / original_size) * 100
        
        return original_size, optimized_size, True
    
    except Exception as e:
        print(f"  ❌ Error processing {os.path.basename(image_path)}: {str(e)}")
        return 0, 0, False

def main():
    """Main optimization function"""
    print("=" * 70)
    print("🖼️  MEDDY TOURS IMAGE OPTIMIZATION SCRIPT")
    print("=" * 70)
    print()
    
    # Create backup
    if not os.path.exists(BACKUP_DIR):
        print("📦 Creating backup of original images...")
        shutil.copytree(ASSETS_DIR, BACKUP_DIR)
        print(f"   ✓ Backup created at: {BACKUP_DIR}")
        print()
    
    if not os.path.exists(ASSETS_DIR):
        print(f"❌ Assets directory not found: {ASSETS_DIR}")
        return
    
    # Get all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    image_files = [
        os.path.join(ASSETS_DIR, f)
        for f in os.listdir(ASSETS_DIR)
        if os.path.splitext(f)[1].lower() in image_extensions
    ]
    
    if not image_files:
        print("No images found to optimize!")
        return
    
    print(f"📊 Found {len(image_files)} image(s) to optimize")
    print()
    
    total_original = 0
    total_optimized = 0
    successful = 0
    failed = 0
    
    for image_path in sorted(image_files):
        filename = os.path.basename(image_path)
        original_size, optimized_size, success = optimize_image(image_path)
        
        total_original += original_size
        total_optimized += optimized_size
        
        if success:
            successful += 1
            compression = (1 - optimized_size / original_size) * 100 if original_size > 0 else 0
            status = "✓" if compression > 0 else "→"
            print(f"{status} {filename:45} {format_size(original_size):>12} → {format_size(optimized_size):>12} ({compression:>5.1f}%)")
        else:
            failed += 1
    
    print()
    print("=" * 70)
    print(f"OPTIMIZATION COMPLETE")
    print("=" * 70)
    print(f"✓ Successfully optimized: {successful}")
    print(f"❌ Failed: {failed}")
    print()
    print(f"📊 TOTAL SAVINGS:")
    print(f"   Original size:  {format_size(total_original)}")
    print(f"   Optimized size: {format_size(total_optimized)}")
    total_saved = total_original - total_optimized
    total_percent = (total_saved / total_original * 100) if total_original > 0 else 0
    print(f"   Saved:          {format_size(total_saved)} ({total_percent:.1f}%)")
    print()
    print("✅ Website is now optimized for faster loading!")
    print()

if __name__ == '__main__':
    main()
