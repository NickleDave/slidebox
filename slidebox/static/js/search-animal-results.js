$(function() {
    $('.inject_info').each(function(){
            var reducedHeight = $(this).height();
            $(this).css('height', 'auto');
            var fullHeight = $(this).height();
            $(this).height(reducedHeight);
            
            $(this).data('reducedHeight', reducedHeight);
            $(this).data('fullHeight', fullHeight);
            });
    $('<a />', {
        href: '#',
        class: 'moreLink',
        text: 'More...'
    }).appendTo('.inject_info')
        .click(function() {
            $e = $(this).parent();
            if ($e.height() == $e.data('reducedHeight')) {
                $e.animate({height: $e.data('fullHeight')}, 500);
                }
            else {
                $e.animate({height: $e.data('reducedHeight')}, 500);;
                }
            });
});
