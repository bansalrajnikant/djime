/* JavaScript common to the entire Djime app. */

$(document).ready(function () {
    // Message sendt from django auth messaging.
    $("#content #messages li")
    // Add a close button
    .prepend('<span class="close">&times;</span>')
    // Rounded corners
    .corner()
    // And hide it on click
    .click(function () {
        $(this).fadeOut()
    });
});

