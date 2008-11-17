/* Misc. bindings and functions for the tracker HTML-pages */
$(document).ready(function () {
  $("div.ui-dialog").hide();

  $("#delete-slip-button").click(function () {
    $("#delete-dialog-box").dialog({
      buttons: {
        "Delete this slip": function() {
            $.delete_('/tracker/slip/1');
            $(this).dialog("close");
        },
        "Cancel": function() {
            $(this).dialog("close");
        }
      }
    });
  });
});
