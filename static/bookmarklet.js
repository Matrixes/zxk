// find images and display them
$.each($('img[src$="jpg"]'), function(index, image) {
	if ($(image).width() >= 100 && jQuery(image).height() >= 100) {
		image_url = $(image).attr('src');
		$('#bookmarklet .images').append('<a href="#"><img src="'+ image_url +'" /></a>');
	}
});


$('#bookmarklet .images a').click(function(e){
	selected_image = jQuery(this).children('img').attr('src');
	// hide bookmarklet
	$('#bookmarklet').hide();
	// open new window to submit the image
	window.open(site_url +'images/create/?url=' + encodeURIComponent(selected_image) + '&title=' + encodeURIComponent(jQuery('title').text()),'_blank');
});

