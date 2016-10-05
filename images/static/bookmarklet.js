var site_url = 'http://127.0.0.1:8000/';
var static_url = site_url + 'static/';
var min_width = 100;
var min_height = 100;

// find images and display them
$.each($('img[src$="jpg"]'), function(index, image) {
	if ($(image).width() >= min_width && jQuery(image).height() >= min_height) {
		image_url = jQuery(image).attr('src');
		jQuery('#bookmarklet .images').append('<a href="#"><img src="'+ image_url +'" /></a>');
	}
});