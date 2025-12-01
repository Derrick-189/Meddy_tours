#!/usr/bin/env python3
"""
Quick image optimization script for new images
Run this whenever you add new images to optimize them for web
"""

import os
import sys
from PIL import Image
from pathlib import Path

def optimize_single_image(filepath):
    """Optimize a single image file"""
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return
    
    original_size = os.path.getsize(filepath)
    print(f"Optimizing: {os.path.basename(filepath)} ({original_size / 1024:.1f} KB)...")
    
    try:
        img = Image.open(filepath)
        
        # Convert RGBA to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        
        # Resize if too large
        if img.width > 1920 or img.height > 1080:
            img.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
        
        # Save optimized
        file_ext = os.path.splitext(filepath)[1].lower()
        if file_ext in ['.jpg', '.jpeg']:
            img.save(filepath, 'JPEG', quality=85, optimize=True)
        elif file_ext == '.png':
            img.save(filepath, 'PNG', optimize=True)
        
        optimized_size = os.path.getsize(filepath)
        compression = (1 - optimized_size / original_size) * 100
        
        print(f"✓ {os.path.basename(filepath)}: {original_size/1024:.1f} KB → {optimized_size/1024:.1f} KB ({compression:.1f}% saved)")
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 optimize_single_image.py <image_path>")
        print("Example: python3 optimize_single_image.py assets/images/my_image.jpg")
        sys.exit(1)
    
    optimize_single_image(sys.argv[1])
