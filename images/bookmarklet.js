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
		})
	}
}) ();