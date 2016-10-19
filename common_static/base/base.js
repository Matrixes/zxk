

$('.navbar').hover(function() {
	$(this).css('background-color', '#E8E8E8');
    },function(){
    $(this).css('background-color', 'transparent');
})


$('.navbar-nav>li a').hover(function() {
	$(this).css({'font-style': 'italic', 'font-weight': 'bold'});
    },function(){
    $(this).css({'font-style': 'normal', 'font-weight': 'normal'});
})



/*
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
*/

/*
$("#username").on('blur', function() {
	var username = $(this).val();

	$.post("accounts/ajax-login/",
	    {
	    	username: username,
	    },
	    function(res) {
	    	$("#msg").html(res);
	});
});

$("#ajax-submit").on('submit', function() {
	var username = $("#username").val()
	var password = $("#password").val()

	$.post("accounts/ajax-login/",
	    {
	    	username: username,
	    	password: password,
	    },
	    function(res) {
	    	$("#msg").html(res);
	    });
});
*/

/*============================================*/

