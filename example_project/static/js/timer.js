$(document).ready(function () {
	var both_timers = $('#slip-timer-button, #slip-timer-sidebar-button')
	$('#slip-timer-button.timer-running, #slip-timer-sidebar-button.timer-running').timeclock({since: djime.current_time});


	$('#slip-timer-button, #slip-timer-sidebar-button').click(function () {
	  if ($(this).hasClass($.timeclock.markerClassName)) {
	    var elapsed = both_timers.timeclock('destroy');
	    $.post('/slip/' + djime.slip_id + '/stop/', {elapsed: elapsed});
	    $.getJSON('/slip/' + djime.slip_id + '/get_json/', function(data) {
	      $("#slip-total-time").text(data.slip_time);
	    });
	  }
	  else {
	    $.post('/slip/' + djime.slip_id + '/start/');
	    both_timers.timeclock();
	  }
	});
});