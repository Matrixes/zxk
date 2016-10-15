/*
$("#likes").one('click', function() {
	var postid = $(this).attr("data-postid");
	$.get("/blog/post_like/", {post_id: postid}, function(data){
		$('#like_count').html(data);
	});
})