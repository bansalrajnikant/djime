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

  $.getJSON(document.URL + 'get_json/', function(data, textStatus) {
    $("#timer").val(data.slip_time);
    if (data.active == true) {
      $("#start-stop-button").val('Start');
    }
    else {
      $("#start-stop-button").val('Stop');
    }

  });

  $("#start-stop-button").click(function () {
    if ((this).value == 'Start') {
      (this).value = 'Stop'
      $.post(document.URL + 'start/', function(data) {
      });
    }
    else if ((this).value == 'Stop') {
      (this).value = 'Start'
      $.post(document.URL + 'stop/', function(data) {
      });
      $.getJSON(document.URL + 'get_json/', function(data) {
        $("#timer").val(data.slip_time);
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
