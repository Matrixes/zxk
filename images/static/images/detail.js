
$(function() {
    $('#like').on('click', function(e) {
        e.preventDefault();
        $.post('/images/like/', {
            id: $(this).data('id'),
            action: $(this).data('action')
        }, function(data) {
            if (data['status'] == 'ok') {
                var previous_action = $('#like').data('action');

                // toggle data-action
                $('#like').data('action', previous_action == 'like' ? 'unlike' : 'like');
                
                // toggle link text
                $('.like-button').text(previous_action == 'like' ? '取消喜欢' : '喜欢');

                // update total likes
                var previous_likes = parseInt($('span.like-count').text());
                $('span.like-count').text(previous_action == 'like' ? previous_likes + 1 : previous_likes - 1);
            }
        })
    })
})
