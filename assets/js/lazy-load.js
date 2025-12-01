/**
 * Lazy Loading Module for Meddy Tours
 * Handles image lazy loading using Intersection Observer API
 * Falls back to data-src attribute for older browsers
 */

const LazyLoadManager = {
  init: function() {
    // Check if Intersection Observer is supported
    if ('IntersectionObserver' in window) {
      this.initIntersectionObserver();
    } else {
      this.initFallback();
    }
    
    // Check WebP support
    this.checkWebPSupport();
  },
  
  /**
   * Initialize Intersection Observer for modern browsers
   */
  initIntersectionObserver: function() {
    const imageElements = document.querySelectorAll('img[data-src], img[data-lazy]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          const src = img.dataset.src || img.dataset.lazy;
          const srcset = img.dataset.srcset;
          
          // Load the image
          if (src) {
            img.src = src;
          }
          if (srcset) {
            img.srcset = srcset;
          }
          
          // Handle picture element sources
          const picture = img.closest('picture');
          if (picture) {
            const sources = picture.querySelectorAll('source[data-srcset]');
            sources.forEach(source => {
              source.srcset = source.dataset.srcset;
              source.removeAttribute('data-srcset');
            });
          }
          
          // Remove data attributes and add loaded class
          img.removeAttribute('data-src');
          img.removeAttribute('data-lazy');
          img.removeAttribute('data-srcset');
          img.classList.add('loaded');
          img.classList.add('image-fade-in');
          
          // Stop observing this element
          observer.unobserve(img);
        }
      });
    }, {
      rootMargin: '50px' // Start loading 50px before image enters viewport
    });
    
    imageElements.forEach(img => imageObserver.observe(img));
  },
  
  /**
   * Fallback for older browsers without Intersection Observer
   */
  initFallback: function() {
    const imageElements = document.querySelectorAll('img[data-src], img[data-lazy]');
    
    imageElements.forEach(img => {
      const src = img.dataset.src || img.dataset.lazy;
      if (src) {
        img.src = src;
      }
      img.classList.add('loaded');
    });
  },
  
  /**
   * Check WebP support and add class to body
   */
  checkWebPSupport: function() {
    const webP = new Image();
    webP.onload = webP.onerror = function() {
      if (webP.height === 2) {
        document.body.classList.add('image-webp-support');
      } else {
        document.body.classList.add('image-no-webp-support');
      }
    };
    webP.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAAA/AQAIBAQABQACAAA==';
  },
  
  /**
   * Manually load an image (useful for dynamic content)
   */
  loadImage: function(element) {
    if (element.dataset.src) {
      element.src = element.dataset.src;
      element.removeAttribute('data-src');
      element.classList.add('loaded');
    }
  }
};

// Initialize on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', function() {
    LazyLoadManager.init();
  });
} else {
  LazyLoadManager.init();
}
