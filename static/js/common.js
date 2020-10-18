$(function() {

    // Sticky Element on scroll
    var sticky = $('header.sticky');
    var fixed = $('header.fixed');
	var top = fixed.offset().top - parseFloat(fixed.css('margin-top').replace(/auto/, 0));
	$(window).scroll(function (event) {
        var y = $(this).scrollTop();
        if (y > top){
            sticky.removeClass('hide')
            fixed.addClass('hide')
        } else {
            sticky.addClass('hide')
            fixed.removeClass('hide')
        }
    });
    
});