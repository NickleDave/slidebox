$(function() {
    $('.expand').each(function(){
        var reducedHeight = $(this).height();
        $(this).css('height', 'auto');
        var fullHeight = $(this).height();
        $(this).height(reducedHeight);
        
        $(this).data('reducedHeight', reducedHeight);
        $(this).data('fullHeight', fullHeight);
    }).click(function() {
        $(this).animate({height: $(this).height() == $(this).data('reducedHeight') ? $(this).data('fullHeight') : $(this).data('reducedHeight')}, 500);
    });
});
