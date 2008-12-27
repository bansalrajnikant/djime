/* JavaScript common to the entire Djime app. */

$(document).ready(function () {
    $("#content #messages li").click(function () {
        $(this).fadeOut()
    });
});

