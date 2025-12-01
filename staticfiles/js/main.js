AOS.init({
    duration: 850,
    easing: 'ease-out-cubic',
    once: false
});

jQuery(document).ready(function($) {

	"use strict";
	

	var siteMenuClone = function() {

		$('.js-clone-nav').each(function() {
			var $this = $(this);
			$this.clone().attr('class', 'site-nav-wrap').appendTo('.site-mobile-menu-body');
		});


		setTimeout(function() {
			
			var counter = 0;
      $('.site-mobile-menu .has-children').each(function(){
        var $this = $(this);
        
        $this.prepend('<span class="arrow-collapse collapsed">');

        $this.find('.arrow-collapse').attr({
          'data-toggle' : 'collapse',
          'data-target' : '#collapseItem' + counter,
        });

        $this.find('> ul').attr({
          'class' : 'collapse',
          'id' : 'collapseItem' + counter,
        });

        counter++;

      });

    }, 1000);

		$('body').on('click', '.arrow-collapse', function(e) {
      var $this = $(this);
      if ( $this.closest('li').find('.collapse').hasClass('show') ) {
        $this.removeClass('active');
      } else {
        $this.addClass('active');
      }
      e.preventDefault();  
      
    });

		$(window).resize(function() {
			var $this = $(this),
				w = $this.width();

			if ( w > 768 ) {
				if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
				}
			}
		})

		$('body').on('click', '.js-menu-toggle', function(e) {
			var $this = $(this);
			e.preventDefault();

			if ( $('body').hasClass('offcanvas-menu') ) {
				$('body').removeClass('offcanvas-menu');
				$this.removeClass('active');
			} else {
				$('body').addClass('offcanvas-menu');
				$this.addClass('active');
			}
		}) 

		// click outisde offcanvas
		$(document).mouseup(function(e) {
	    var container = $(".site-mobile-menu");
	    if (!container.is(e.target) && container.has(e.target).length === 0) {
	      if ( $('body').hasClass('offcanvas-menu') ) {
					$('body').removeClass('offcanvas-menu');
				}
	    }
		});
	}; 
	siteMenuClone();


	var sitePlusMinus = function() {
		$('.js-btn-minus').on('click', function(e){
			e.preventDefault();
			if ( $(this).closest('.input-group').find('.form-control').val() != 0  ) {
				$(this).closest('.input-group').find('.form-control').val(parseInt($(this).closest('.input-group').find('.form-control').val()) - 1);
			} else {
				$(this).closest('.input-group').find('.form-control').val(parseInt(0));
			}
		});
		$('.js-btn-plus').on('click', function(e){
			e.preventDefault();
			$(this).closest('.input-group').find('.form-control').val(parseInt($(this).closest('.input-group').find('.form-control').val()) + 1);
		});
	};
	// sitePlusMinus();


	var siteSliderRange = function() {
    $( "#slider-range" ).slider({
      range: true,
      min: 0,
      max: 500,
      values: [ 75, 300 ],
      slide: function( event, ui ) {
        $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
      }
    });
    $( "#amount" ).val( "$" + $( "#slider-range" ).slider( "values", 0 ) +
      " - $" + $( "#slider-range" ).slider( "values", 1 ) );
	};
	// siteSliderRange();


	var siteMagnificPopup = function() {
		$('.image-popup').magnificPopup({
	    type: 'image',
	    closeOnContentClick: true,
	    closeBtnInside: false,
	    fixedContentPos: true,
	    mainClass: 'mfp-no-margins mfp-with-zoom', // class to remove default margin from left and right side
	     gallery: {
	      enabled: true,
	      navigateByImgClick: true,
	      preload: [0,1] // Will preload 0 - before current, and 1 after the current image
	    },
	    image: {
	      verticalFit: true
	    },
	    zoom: {
	      enabled: true,
	      duration: 300 // don't foget to change the duration also in CSS
	    }
	  });

	  $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
	    disableOn: 700,
	    type: 'iframe',
	    mainClass: 'mfp-fade',
	    removalDelay: 160,
	    preloader: false,

	    fixedContentPos: false
	  });

	  // Local inline video popup
	  $('.popup-local-video').magnificPopup({
	    type: 'inline',
	    midClick: true,
	    closeBtnInside: true,
	    closeOnBgClick: true,
	    enableEscapeKey: true,
	    callbacks: {
	      open: function() {
	        var video = document.getElementById('promoVideoEl');
	        if (video) {
	          video.currentTime = 0;
	          video.play();
	          // Auto-close when video ends
	          video._mfpOnEndedHandler = function() {
	            $.magnificPopup.close();
	          };
	          video.addEventListener('ended', video._mfpOnEndedHandler);
	        }
	      },
	      close: function() {
	        var video = document.getElementById('promoVideoEl');
	        if (video) {
	          video.pause();
	          // Remove the ended listener to avoid leaks
	          if (video._mfpOnEndedHandler) {
	            video.removeEventListener('ended', video._mfpOnEndedHandler);
	            delete video._mfpOnEndedHandler;
	          }
	        }
	      }
	    }
	  });

	  // Gallery: open local MP4s in an inline modal
	  $('.popup-video').magnificPopup({
	    type: 'inline',
	    midClick: true,
	    closeBtnInside: true,
	    closeOnBgClick: true,
	    enableEscapeKey: true,
	    callbacks: {
	      open: function() {
	        var $el = this.st.el;
	        var src = $el.attr('href');
	        var title = $el.data('title') || '';
	        var markup = [
	          '<div class="video-popup">',
	            title ? ('<h3 class="mb-3">' + title + '</h3>') : '',
	            '<video controls playsinline preload="metadata">',
	              '<source src="' + src + '" type="video/mp4">',
	              'Your browser does not support the video tag.',
	            '</video>',
	          '</div>'
	        ].join('');
	        this.content.html(markup);
	      }
	    }
	  });
	};
	siteMagnificPopup();


	var siteCarousel = function () {
		if ( $('.nonloop-block-13').length > 0 ) {
			$('.nonloop-block-13').owlCarousel({
		    center: false,
		    items: 1,
		    loop: true,
				stagePadding: 0,
		    margin: 0,
		    autoplay: true,
		    nav: true,
				navText: ['<span class="icon-arrow_back">', '<span class="icon-arrow_forward">'],
		    responsive:{
	        600:{
	        	margin: 0,
	          items: 1
	        },
	        1000:{
	        	margin: 0,
	        	stagePadding: 0,
	          items: 1
	        },
	        1200:{
	        	margin: 0,
	        	stagePadding: 0,
	          items: 1
	        }
		    }
			});
		}

		$('.slide-one-item').owlCarousel({
	    center: false,
	    items: 1,
	    loop: true,
			stagePadding: 0,
	    margin: 0,
	    autoplay: true,
	    pauseOnHover: false,
	    nav: true,
	    navText: ['<span class="icon-keyboard_arrow_left">', '<span class="icon-keyboard_arrow_right">']
	  });
	};
	siteCarousel();

	var siteStellar = function() {
		$(window).stellar({
	    responsive: false,
	    parallaxBackgrounds: true,
	    parallaxElements: true,
	    horizontalScrolling: false,
	    hideDistantElements: false,
	    scrollProperty: 'scroll'
	  });
	};
	siteStellar();

	var siteCountDown = function() {

		$('#date-countdown').countdown('2020/10/10', function(event) {
		  var $this = $(this).html(event.strftime(''
		    + '<span class="countdown-block"><span class="label">%w</span> weeks </span>'
		    + '<span class="countdown-block"><span class="label">%d</span> days </span>'
		    + '<span class="countdown-block"><span class="label">%H</span> hr </span>'
		    + '<span class="countdown-block"><span class="label">%M</span> min </span>'
		    + '<span class="countdown-block"><span class="label">%S</span> sec</span>'));
		});
				
	};
	siteCountDown();

	var siteDatePicker = function() {

		if ( $('.datepicker').length > 0 ) {
			$('.datepicker').datepicker();
		}

	};
	siteDatePicker();
	// Equalize heights for common image-card patterns per row
	(function equalizeAllImageGroups(){
	  function debounce(fn, wait){ var t; return function(){ clearTimeout(t); t = setTimeout(fn, wait); }; }

	  // Supported patterns and grouping
	  var PATTERNS = [
    { card: '.unit-1',                img: '.unit-1 img',                    groupBy: function($el){ return $el.closest('.row'); } },
    { card: '.country-item .rounded', img: '.country-item .rounded img',     groupBy: function($el){ return $el.closest('.row'); } }
  ];

	  function groups(){
	    var set = [];
	    PATTERNS.forEach(function(p){
	      $(p.card).each(function(){
	        var $el = $(this);
	        var $group = p.groupBy ? p.groupBy($el) : $el.closest('.row');
	        if ($group && $group.length && set.indexOf($group[0]) === -1) set.push($group[0]);
	      });
	    });
	    return $(set);
	  }

	  function syncGroup($group){
	    PATTERNS.forEach(function(p){
	      var $cards = $group.find(p.card);
	      var $imgs  = $group.find(p.img);
	      if (!$cards.length || !$imgs.length) return;
	      $cards.css('height','');
	      $imgs.css('height','');
	      var maxH = 0;
	      $imgs.each(function(){ var h = this.clientHeight || $(this).height(); if (h > maxH) maxH = h; });
	      if (maxH > 0) { $cards.css('height', maxH + 'px'); $imgs.css('height','100%'); }
	    });
	  }

	  function syncAll(){ groups().each(function(){ syncGroup($(this)); }); }

	  function initialize(){
	    var $groups = groups();
	    if (!$groups.length) return;
	    var pending = 0;
	    $groups.each(function(){
	      var $grp = $(this);
	      PATTERNS.forEach(function(p){ pending += $grp.find(p.img).length; });
	    });
	    if (!pending) { syncAll(); return; }
	    $groups.each(function(){
	      var $grp = $(this);
	      PATTERNS.forEach(function(p){
	        $grp.find(p.img).each(function(){
	          if (this.complete) { if(--pending===0) syncAll(); }
	          else { $(this).one('load error', function(){ if(--pending===0) syncAll(); }); }
	        });
	      });
	    });
	  }

	  initialize();
	  $(window).on('resize', debounce(syncAll, 150));
	  $(window).on('load', syncAll);

	  // Testimonials: equalize to the smallest image height
	  (function equalizeTestimonials(){
	    var $imgs = $('.nonloop-block-13 .item img.img-md-fluid');
	    if (!$imgs.length) return;
	    function run(){
	      $imgs.css('height','');
	      var minH = Infinity;
	      $imgs.each(function(){ var h = this.clientHeight || $(this).height(); if (h && h < minH) minH = h; });
	      if (isFinite(minH) && minH > 0) { $imgs.css('height', minH + 'px'); }
	    }
	    var pending = $imgs.length;
	    $imgs.each(function(){ if (this.complete) { if(--pending===0) run(); } else { $(this).one('load error', function(){ if(--pending===0) run(); }); } });
	    $(window).on('resize', debounce(run, 150));
	  })();
	})();

	// Gallery: filters, search, pagination (videos.html)
	(function galleryEnhancements(){
	  var $grid = $('#gallery-grid');
	  if (!$grid.length) return; // only on videos.html

	  var $cards = $grid.children('.gallery-card');
	  var $controls = $('.gallery-controls');
	  var pageSize = parseInt($controls.data('page-size') || 9, 10);
	  var state = { filter: '*', query: '', page: 1, pages: 1 };

	  // Build category buttons from data-category
	  var cats = {};
	  $cards.each(function(){ var c = ($(this).data('category')||'Uncategorized').toString(); cats[c] = true; });
	  var $filters = $('.gallery-filters');
	  Object.keys(cats).sort().forEach(function(c){
	    var btn = $('<button/>', { type:'button', class:'btn btn-outline-primary', text:c, 'data-filter': c });
	    $filters.append(btn);
	  });

	  function apply(){
	    // Filter by category and text
	    var q = state.query.toLowerCase();
	    var shown = [];
	    $cards.each(function(){
	      var $el = $(this);
	      var matchCat = (state.filter === '*') || ($el.data('category')+'' === state.filter);
	      var title = ($el.data('title')||'').toString().toLowerCase();
	      var desc  = ($el.data('desc')||'').toString().toLowerCase();
	      var matchText = !q || title.indexOf(q) !== -1 || desc.indexOf(q) !== -1;
	      if (matchCat && matchText) { shown.push($el); $el.show(); } else { $el.hide(); }
	    });
	    // Pagination
	    state.pages = Math.max(1, Math.ceil(shown.length / pageSize));
	    if (state.page > state.pages) state.page = 1;
	    // Show only current page items
	    shown.forEach(function($el, idx){
	      var pageIndex = Math.floor(idx / pageSize) + 1;
	      if (pageIndex === state.page) $el.show(); else $el.hide();
	    });
	    renderPagination();
	  }

	  function renderPagination(){
	    var $pager = $('.gallery-pagination');
	    if (!$pager.length) return;
	    $pager.empty();
	    if (state.pages <= 1) return;
	    var $ul = $('<div class="btn-group btn-group-sm" role="group"/>');
	    for (var i=1;i<=state.pages;i++){
	      var $b = $('<button/>', { class:'btn btn-outline-primary' + (i===state.page?' active':''), text:i });
	      (function(page){ $b.on('click', function(){ state.page = page; apply(); window.scrollTo({top: $grid.offset().top - 120, behavior:'smooth'}); }); })(i);
	      $ul.append($b);
	    }
	    $pager.append($ul);
	  }

	  // Events
	  $filters.on('click', 'button', function(){
	    $filters.find('button').removeClass('active');
	    $(this).addClass('active');
	    state.filter = $(this).data('filter');
	    state.page = 1;
	    apply();
	  });
	  $('#gallery-search').on('input', function(){ state.query = $(this).val(); state.page = 1; apply(); });

	  // Initial
	  apply();
	})();
});