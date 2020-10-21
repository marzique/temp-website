$(function() {
    $('.field .player').on('click', function() {
        $('.field .player').removeClass('selected');
        $(this).addClass('selected');
        $('#players').selectric('open').removeClass('hidden');
   });

    var player = null;

    $('#players').selectric({
        onOpen: function() {
            player = $('.field .player.selected')
        },
        onChange: function(element) {
            var number = $("#players :selected").val();
            var surname = $("#players :selected").data('surname');

            player.find('h2').text(number)
            player.find('h3').text(surname)
            $('.field .player').removeClass('selected');
            console.log($(this));
        },
    });

});