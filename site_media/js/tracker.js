/* Misc. bindings and functions for the tracker HTML-pages */
$(document).ready(function () {
  $("div.ui-dialog").hide();

  $("#delete-slip-button").click(function () {
    var dialog_box = $("#dialog-box");
    dialog_box.dialog({
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
      },
      draggable: false,
      modal: false,
      resizable: false,
      show: 'size',
      title: djime.messages.slip_delete_title
    });
    dialog_box.text(djime.messages.slip_delete_body);
  });

  $("#start-stop-button").click(function () {
    if ((this).value == 'Start') {
      (this).value = 'Stop'
      $.post(document.URL + 'start/');
    }
    else if ((this).value == 'Stop') {
      (this).value = 'Start'
      $.post(document.URL + 'stop/');
      $.getJSON(document.URL + 'get_json/', function(data) {
        $("#slip-total-time").text(data.slip_time);
      });

    }
    else {
      alert('something is wrong')
    };

  });

  $("#create-slip").click(function () {
    $.post(document.URL + 'slip/add/', {name: $("#slip-name").val()}, function(data) {
      $.getJSON(document.URL + 'slip/add/', function(data) {
        document.location.href = '/tracker/slip/' + data.slip
      });
    });
  });

  $('.edit').editable(document.URL, {
    indicator : 'Saving...',
    tooltip   : 'Click to edit...',
    name: 'name'
  });
});
