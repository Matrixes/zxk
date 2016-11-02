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

$(function () {
	//收藏
	$('#collect').on('click', function(e) {
		e.preventDefault();
		$.post('/accounts/collecting/',
		{
			id: $(this).data('id'),
			action: $(this).data('action')
		}, function(data) {
			if (data['status'] == 'ok') {
				var previous_action = $('#collect').data('action');

				$('#collect').data('action',
						previous_action == 'collect' ? 'cancel': 'collect');

				$('#collect-text').text(
						previous_action == 'collect' ? '取消收藏' : '收藏');

				var previous_collectors = parseInt($('#collect-count').text());
					$('#collect-count').text(previous_action == 'collect' ? previous_collectors + 1 : previous_collectors - 1);
			}
		}
		);
	});
})