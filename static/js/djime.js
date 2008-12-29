/* JavaScript common to the entire Djime app. */

$(document).ready(function () {
    // Add rounded corners and a "close" button.
    $("#content #messages li")
    .prepend('<span class="close">&times;</span>')
    .corner();
    $("#content #messages li").click(function () {
        $(this).fadeOut()
    });
});

