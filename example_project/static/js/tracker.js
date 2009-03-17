/* Misc. bindings and functions for the tracker HTML-pages */
$(document).ready(function () {
  $("div.ui-dialog").hide();

  $("#delete-slip-button").click(function () {
    $("#main").before('<div id="delete-dialog" class="ui-dialog"/>');
    var dialog_box = $("div#delete-dialog");
    dialog_box.dialog({
      buttons: {
        "Delete this slip": function() {
          $.delete_(document.URL, {}, function (data, textStatus){
            if (textStatus == "success") {
              // If deleting succeeds, redirect to the tracker index page.
              document.location.href = '/slip/'
            }
          });
          $(this).dialog("close");
        },
        "Cancel": function() {
          $(this).dialog("close");
        }
      },
      bgiframe: true,
      draggable: false,
      modal: true,
      resizable: false,
      //show: 'size',
      title: djime.messages.slip_delete_title
    });
    dialog_box.text(djime.messages.slip_delete_body);
  });

  $('.edit').editable(document.URL, {
    indicator : 'Saving...',
    tooltip   : 'Click to edit...',
    name: 'name'
  });
});
