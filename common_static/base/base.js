$(".navbar").on('mouseenter', function(){
	$(this).css('background-color', '#E8E8E8');
});

$(".navbar").on('mouseleave', function(){
	$(this).css('background-color', '#FFFFFF');
});


$("ul.nav li").on('mouseenter', function(){
	$(this).css({'font-style': 'italic', 'font-weight': 'bold'});
});

$("ul.nav li").on('mouseleave', function(){
	$(this).css({'font-style': 'normal', 'font-weight': 'normal'});
});


var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
}
}
});


$('#ajax-submit').on('click', function() {
	$.post('/accounts/ajax-login/',
	    {
	    	username: $('#username').val(),
	    	password: $('#password').val(),
	    });
});