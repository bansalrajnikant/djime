/* Misc. bindings and functions for the tracker HTML-pages */
$(document).ready(function () {
  $("div.ui-dialog").hide();

  $("#delete-slip-button").click(function () {
    $("#delete-dialog-box").dialog({
      buttons: {
        "Delete this slip": function() {
          $.delete_(document.URL, {}, function (data, textStatus){
            if (textStatus == "success") {
              // If deleting succeeds, redirect to the tracker index page.
              document.location.href = '/tracker/'
            }
          });
          $(this).dialog("close");

        },
        "Cancel": function() {
          $(this).dialog("close");
        }
      }
    });
  });
});
