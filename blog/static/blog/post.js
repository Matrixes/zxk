$(function() {
	$('#like').one('click', function() {
		$.post("/blog/post-like/", 
			{
				post_id: $(this).data('id'),
			},
			function(data) {
				$('#like_count').text(data['count']);
			});
	});
	//$("#comments").click
});

