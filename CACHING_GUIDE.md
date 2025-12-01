# Django Caching Configuration for Meddy Tours
# Add this to your settings.py or create a separate config file

"""
DJANGO CACHING SETUP FOR MEDDY TOURS
=====================================

This configuration file provides optimal caching settings for production deployment.
Choose the appropriate configuration based on your hosting setup.
"""

# =============================================================================
# OPTION 1: DJANGO CACHE FRAMEWORK WITH LOCMEM (Development/Testing)
# =============================================================================
# Use this for local development and testing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'meddy-tours-cache',
        'TIMEOUT': 300,  # 5 minutes
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# =============================================================================
# OPTION 2: REDIS CACHING (Production - Recommended)
# =============================================================================
# Requires: pip install django-redis
# Use this for production with Redis server
"""
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            'IGNORE_EXCEPTIONS': True,
        },
        'KEY_PREFIX': 'meddy_tours',
        'TIMEOUT': 300,
    }
}
"""

# =============================================================================
# OPTION 3: DATABASE CACHING (Production Alternative)
# =============================================================================
# Use this if you don't have Redis
# Run: python manage.py createcachetable
"""
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 5000
        }
    }
}
"""

# =============================================================================
# HTTP CACHE HEADERS
# =============================================================================
# Add to settings.py to enable HTTP caching in browser and CDN

# Static files caching (images, CSS, JS)
STATIC_FILES_CACHE_TIMEOUT = 86400 * 30  # 30 days for images
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Middleware to add cache headers
MIDDLEWARE = [
    # ... other middleware ...
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    # ... rest of middleware ...
]

# Cache timeout for pages (in seconds)
CACHE_MIDDLEWARE_SECONDS = 600  # 10 minutes

# =============================================================================
# WHITENOISE CONFIGURATION (For Static File Serving)
# =============================================================================
# Requires: pip install whitenoise
# Add to MIDDLEWARE at the top:
# 'whitenoise.middleware.WhiteNoiseMiddleware',

# Enable compression and caching with WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =============================================================================
# RESPONSE HEADERS FOR CACHING
# =============================================================================
# Add this middleware class to set cache headers:

"""
# create_file: middleware/cache_headers.py
from django.utils.decorators import decorator_from_middleware
from django.utils.cache import add_never_cache_headers, patch_response_headers

class CacheHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Cache static files for 30 days
        if request.path.startswith('/static/'):
            patch_response_headers(response, cache_timeout=2592000)
        
        # Cache media files for 7 days
        elif request.path.startswith('/media/'):
            patch_response_headers(response, cache_timeout=604800)
        
        # Don't cache HTML pages (or cache for shorter period)
        elif request.path == '/' or request.path.endswith('.html'):
            patch_response_headers(response, cache_timeout=600)
        
        return response
"""

# =============================================================================
# GZIP COMPRESSION
# =============================================================================
# Add to settings.py

MIDDLEWARE = [
    # ... other middleware ...
    'django.middleware.gzip.GZipMiddleware',
    # ... rest of middleware ...
]

# Enable gzip compression for responses larger than 1.4KB
GZIP_MINIMUM_LENGTH_BYTES = 1400

# =============================================================================
# SECURITY & PERFORMANCE HEADERS
# =============================================================================

# Content Security Policy
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'style-src': ("'self'", "'unsafe-inline'", "fonts.googleapis.com"),
    'script-src': ("'self'", "'unsafe-inline'"),
    'img-src': ("'self'", "data:", "https:"),
}

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY_REPORT_ONLY = False
X_FRAME_OPTIONS = 'DENY'

# HTTPS configuration (for production)
SECURE_SSL_REDIRECT = True  # Only in production!
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# =============================================================================
# IMPLEMENTATION GUIDE
# =============================================================================
"""
1. CHOOSE YOUR CACHING BACKEND:
   - Development: Use OPTION 1 (LocMemCache)
   - Production: Use OPTION 2 (Redis - recommended) or OPTION 3 (Database)

2. ADD TO settings.py:
   
   # Copy the cache configuration above
   CACHES = { ... }
   
   # Add middleware (in this order)
   MIDDLEWARE = [
       'django.middleware.cache.UpdateCacheMiddleware',
       'django.middleware.common.CommonMiddleware',
       'django.middleware.cache.FetchFromCacheMiddleware',
       'django.middleware.gzip.GZipMiddleware',
   ]
   
   # Enable compression
   GZIP_MINIMUM_LENGTH_BYTES = 1400

3. FOR REDIS (Production):
   
   $ pip install django-redis
   $ redis-server  # Start Redis
   
   Then use OPTION 2 configuration

4. FOR DATABASE CACHING:
   
   $ python manage.py createcachetable

5. TEST CACHING:
   
   $ python manage.py shell
   >>> from django.core.cache import cache
   >>> cache.set('test_key', 'test_value')
   >>> cache.get('test_key')
   'test_value'

6. VERIFY HTTP CACHE HEADERS:
   
   $ curl -I http://localhost:8000/static/css/style.css
   # Look for: Cache-Control, Expires, ETag headers
"""

# =============================================================================
# EXPECTED PERFORMANCE GAINS WITH CACHING
# =============================================================================
"""
Metric                        Improvement
────────────────────────────────────────────
Page Load (repeat visit)      50-80% faster
Server Load Reduction         60-80% less
Database Queries              70-90% fewer
Bandwidth Usage               40-60% less
Time to First Byte (TTFB)     30-50% faster

Key Benefits:
✅ Reduced server load
✅ Faster repeat visits
✅ Lower bandwidth costs
✅ Better user experience
✅ Improved SEO ranking
"""
