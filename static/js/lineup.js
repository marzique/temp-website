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

    $('#download').on('click', function() {
        console.log('downloading lineup')
    });

    $('#download-lineup').on("submit", function(event){
        // Prevent default posting of form - put here to work in case of errors
        event.preventDefault();

        var table_html = $('.field').html()

         // Fire off the request to /form.php
        request = $.ajax({
            url: "/squad/lineup/download/",
            type: "post",
            data: {
                'table_html': table_html
            }
        });

        return false;
      })

    // SHEME
    $('input[type=radio][name=scheme]').change(function() {
        $('.field').removeClass('s442 s451')
        $('.field').addClass(this.value)
        console.log(this.value);
    });

});