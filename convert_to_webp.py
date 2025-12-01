#!/usr/bin/env python3
"""
WebP Image Converter for Meddy Tours
Converts JPEG images to WebP format with fallback support
WebP typically saves an additional 15-25% compared to JPEG
"""

import os
import subprocess
from pathlib import Path
from PIL import Image

ASSETS_DIR = '/home/slade/Meddy_Tours/assets/images'
QUALITY = 85
WEBP_QUALITY = 85

def has_imagemagick():
    """Check if ImageMagick is installed"""
    try:
        subprocess.run(['convert', '--version'], 
                      capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def has_cwebp():
    """Check if cwebp is installed"""
    try:
        subprocess.run(['cwebp', '-version'], 
                      capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def convert_to_webp_pillow(jpg_path):
    """Convert JPEG to WebP using PIL"""
    try:
        img = Image.open(jpg_path)
        webp_path = jpg_path.rsplit('.', 1)[0] + '.webp'
        
        # Convert RGBA to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        
        img.save(webp_path, 'WEBP', quality=WEBP_QUALITY)
        return webp_path, True
    except Exception as e:
        print(f"  ❌ PIL conversion error: {str(e)}")
        return None, False

def convert_to_webp_cwebp(jpg_path):
    """Convert JPEG to WebP using cwebp (better quality)"""
    try:
        webp_path = jpg_path.rsplit('.', 1)[0] + '.webp'
        cmd = ['cwebp', '-quality', str(WEBP_QUALITY), jpg_path, '-o', webp_path]
        result = subprocess.run(cmd, capture_output=True, check=True)
        return webp_path, True
    except Exception as e:
        print(f"  ❌ cwebp conversion error: {str(e)}")
        return None, False

def format_size(bytes):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} GB"

def main():
    print("=" * 70)
    print("🖼️  MEDDY TOURS WEBP CONVERSION SCRIPT")
    print("=" * 70)
    print()
    
    # Check conversion tools
    has_imagemagick_flag = has_imagemagick()
    has_cwebp_flag = has_cwebp()
    
    if not has_cwebp_flag and not has_imagemagick_flag:
        # Fall back to PIL
        print("⚠️  Optional tools not found:")
        if not has_cwebp_flag:
            print("  - cwebp (install: apt-get install webp)")
        if not has_imagemagick_flag:
            print("  - ImageMagick (install: apt-get install imagemagick)")
        print()
        print("Using PIL for conversion (good quality, slower)")
        print()
    else:
        if has_cwebp_flag:
            print("✓ cwebp found (best quality)")
        if has_imagemagick_flag:
            print("✓ ImageMagick found")
        print()
    
    if not os.path.exists(ASSETS_DIR):
        print(f"❌ Assets directory not found: {ASSETS_DIR}")
        return
    
    # Get all JPEG files
    jpg_files = [
        os.path.join(ASSETS_DIR, f)
        for f in os.listdir(ASSETS_DIR)
        if f.lower().endswith(('.jpg', '.jpeg'))
    ]
    
    if not jpg_files:
        print("No JPEG images found to convert!")
        return
    
    print(f"📊 Found {len(jpg_files)} JPEG image(s) to convert to WebP")
    print()
    
    total_jpg_size = 0
    total_webp_size = 0
    successful = 0
    failed = 0
    
    for jpg_path in sorted(jpg_files):
        filename = os.path.basename(jpg_path)
        jpg_size = os.path.getsize(jpg_path)
        total_jpg_size += jpg_size
        
        # Try cwebp first, then PIL
        webp_path = None
        success = False
        
        if has_cwebp_flag:
            webp_path, success = convert_to_webp_cwebp(jpg_path)
        
        if not success:
            webp_path, success = convert_to_webp_pillow(jpg_path)
        
        if success and webp_path and os.path.exists(webp_path):
            webp_size = os.path.getsize(webp_path)
            total_webp_size += webp_size
            savings = (1 - webp_size / jpg_size) * 100
            print(f"✓ {filename:45} {format_size(jpg_size):>12} → {format_size(webp_size):>12} ({savings:>5.1f}%)")
            successful += 1
        else:
            failed += 1
            print(f"❌ {filename:45} Conversion failed")
    
    print()
    print("=" * 70)
    print(f"CONVERSION COMPLETE")
    print("=" * 70)
    print(f"✓ Successfully converted: {successful}")
    print(f"❌ Failed: {failed}")
    print()
    
    if total_webp_size > 0:
        print(f"📊 WEBP SAVINGS:")
        print(f"   Original (JPEG):  {format_size(total_jpg_size)}")
        print(f"   WebP Format:      {format_size(total_webp_size)}")
        saved = total_jpg_size - total_webp_size
        percent = (saved / total_jpg_size * 100) if total_jpg_size > 0 else 0
        print(f"   Saved:            {format_size(saved)} ({percent:.1f}%)")
        print()
    
    print("✅ WebP images created successfully!")
    print()
    print("📝 NEXT STEPS:")
    print("   1. Update HTML to use <picture> elements with WebP")
    print("   2. Add format='image/webp' to picture sources")
    print("   3. Keep JPEG as fallback for older browsers")
    print()
    print("📚 EXAMPLE HTML:")
    print("""
    <picture>
      <source srcset="{% static 'images/image.webp' %}" type="image/webp">
      <source srcset="{% static 'images/image.jpg' %}" type="image/jpeg">
      <img src="{% static 'images/image.jpg' %}" alt="Image" loading="lazy">
    </picture>
    """)
    print()

if __name__ == '__main__':
    main()
