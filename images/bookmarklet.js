(function() {
	var jquery_version = '3.1.0';
	var site_url = 'http://127.0.0.1:8000/';
	var static_url = site_url + 'static/';
	var min_width = 100;
	var min_height = 100;

	function bookmarklet(msg) {
		// Check if jQuery is loaded
		if(typeof window.jQuery != 'undefined') {
			bookmarklet();
		} else {
			// Check for conflicts
			var conflict = typeof window.$ != 'undefined';
			var script = document.createElement('script');
			script.setAttribute('src', 'http://ajax.googleapis.com/ajax/libs/jquery/' + jquery_version + '/jquery.min.js');
			document.getElementsByTagName('head')[0].appendChild(script);
			// create a way to wait until script loading
			var attempts = 15;
			(function() {
				// Check again if jQuery is undefined
				if (typeof window.jQuery == 'undefined') {
					if (--attempts > 0) {
						// Calls himself in a few milliseconds
						window.setTimeout(arguments.callee, 250)
					} else {
						// Too much attempts to load, send error
						alert('An error ocurred while loading jQuery')
					}
				} else {
					bookmarklet();
				}
			}) ();						
		}

		// Load CSS
		var css = jQuery('<link>');
		css.attr({rel: 'stylesheet', href: static_url + 'images/bookmarklet.css?r=' = Math.floor(Math.random()*99999999999999999999)});
		jQuery('head').append(css);

		//Load HTML
		box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a><h1>Select an image to bookmark:</h1><div class="images"></div></div>';
		jQuery('body').append(box_html);

		// Close event
		jQuery('#bookmarklet #close').click(function() {
			jQuery('#bookmarklet').remove();
		});

		// find images and display them
		$.each($('img[src$="jpg"]'), function(index, image) {
			if ($(image).width() >= min_width && $(image).height() >= min_height) {
				var image_url = $(image).attr('src');
				$('#bookmarklet .images').append('<a href="#"><img src="'+ image_url +'" /></a>');
			}
		});

		// // when an image is selected open URL with it
		$('#bookmarklet .images a').click(function(e){
			var selected_image = jQuery(this).children('img').attr('src');
			// hide bookmarklet
			$('#bookmarklet').hide();
			// open new window to submit the image
			window.open(site_url +'images/create/?url=' + encodeURIComponent(selected_image) + '&title=' + encodeURIComponent(jQuery('title').text()),'_blank');
		});

	}
}) ();