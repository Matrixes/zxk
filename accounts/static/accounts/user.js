/* user follow ajax */

$(function() {
	$('a.follow').on('click', function(e) {
		e.preventDefault();
		$.post('/accounts/users/follow/',
			{
				id: $(this).data('id'),
				action: $(this).data('action')
			},
			function(data) {
				if (data['status'] == 'ok') {
					var previous_action = $('a.follow').data('action');
					//toggle data-action
					$('a.follow').data('action',
						previous_action == 'follow' ? 'unfollow': 'follow');
					//toggle link text
					$('a.follow').text(
						previous_action == 'follow' ? '取消关注' : '关注');
					// update total followers
					var previous_followers = parseInt($('#follower-count').text());
					$('#follower-count').text(previous_action == 'follow' ? previous_followers + 1 : previous_followers - 1);
				} 
			}
			)
	})

})

