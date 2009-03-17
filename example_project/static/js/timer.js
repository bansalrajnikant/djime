$(document).ready(function () {
	var both_timers = $('#slip-timer-button, #slip-timer-sidebar-button');

	if (!($('#slip-timer-button').hasClass('timer-added'))) {
		$('#slip-timer-button.timer-running').timeclock({since: djime.current_time}).addClass('timer-added');
		$('#slip-timer-button').addClass('timer-added').click(function () {
		  if ($(this).hasClass($.timeclock.markerClassName)) {
		    var elapsed = both_timers.timeclock('destroy');
		    $.post('/slip/' + djime.slip_id + '/stop/', {elapsed: elapsed});
		    $.getJSON('/slip/' + djime.slip_id + '/get_json/', function(data) {
		      $("#slip-total-time").text(data.slip_time);
		    });
		  }
		  else {
		    $.post('/slip/' + djime.slip_id + '/start/');
				$('#djime-statusbar .content').html('<p>Task: ' + djime.slip_name + '</p><div id="slip-timer-sidebar-button" class="timer-running"><div class="timeclock">0:00</div></div>');
		    both_timers = $('#slip-timer-button, #slip-timer-sidebar-button');
				$('#slip-timer-sidebar-button').addClass('timer-added').click(function () {
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
				both_timers.timeclock();
		  }
		});
	}
	if (!($('#slip-timer-sidebar-button').hasClass('timer-added'))) {
		$('#slip-timer-sidebar-button.timer-running').timeclock({since: djime.current_time}).addClass('timer-added');
		$('#slip-timer-sidebar-button').addClass('timer-added').click(function () {
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
	}
});