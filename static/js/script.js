// scripts.js

$(document).ready(function() {
    $('#sidebar').hover(
        function() {
            $(this).removeClass('collapsed');
        },
        function() {
            $(this).addClass('collapsed');
        }
    );

    $('.toggle-btn').click(function() {
        $('#sidebar').toggleClass('collapsed');
    });
});
// scripts.js

$(document).ready(function() {
    $('.toggle-btn').click(function() {
        $('#sidebar').toggleClass('collapsed');
        $('#page-content-wrapper').toggleClass('collapsed');
    });
});
