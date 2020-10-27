$(function() {

    let good = '#44c379'
    let bad = '#c34444'
    let status = '#44c3bd'

    function notification(text, color){
        Toastify({
            text: text,
            duration: 3000, 
            gravity: "top", // `top` or `bottom`
            position: 'center', // `left`, `center` or `right`
            backgroundColor: color,
            stopOnFocus: true, // Prevents dismissing of toast on hover
            onClick: function(){} // Callback after click
        }).showToast();
    }

    // Sticky HEADER
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

    // Next Match countdown
    if ($('#countdown').length){
        var countdownHtml = $('#countdown');
    }

    // Tabs switcher
    if ($('.tabs').length){

        // thanks to https://denis-creative.com/jquery-tabs/
        $('.tabs').on('click', '.tab:not(.chosen)', function() {
            $(this)
                .addClass('chosen').siblings().removeClass('chosen')
                .closest('.info').find('.wrapper').removeClass('chosen').eq($(this).index()).addClass('chosen');
        });
    }

    // Profile update
    if ($('.user-profile').length){
        $('#enable-edit').on('click', function() {
            $(this).hide();
            $('.user-profile input').prop('disabled', false);
            $('#account #edit-profile, #avatar').show();
       });
    }

    // Like/Dislike 
    if ($('#likes').length){
        $('.triangle').on('click', function() {
            let form = $(this).parent();
            form.submit();
       });
    }
});