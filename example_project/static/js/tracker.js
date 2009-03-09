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
 
  $('#slip-timer-button.timer-running').timeclock({since: djime.current_time});

  $('#slip-timer-button').click(function () {
    if ($(this).hasClass($.timeclock.markerClassName)) {
      var elapsed = $(this).timeclock('destroy');
      $.post(document.URL + 'stop/', {elapsed: elapsed});
      $.getJSON(document.URL + 'get_json/', function(data) {
        $("#slip-total-time").text(data.slip_time);
      });
    }
    else {
      $.post(document.URL + 'start/');
      $(this).timeclock();
    }
  });
});
