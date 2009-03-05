$(document).ready(function () {
	$('#billing-date').datepicker({
    dateFormat: 'yy-mm-dd',
    firstDay: 1,
    maxDate: '1d',
		changeMonth: true,
		changeYear: true,
	});
	$('#id_date').daterangepicker({
    firstDay: 1,
		dateFormat: 'yy-mm-dd',
		doneButtonText: 'Choose',
		presets: {dateRange: 'Custom daterange'},
		presetRanges: [
			{text: 'Last 7 days', dateStart: 'today-7days', dateEnd: 'today' },
			{text: 'Month to date', dateStart: function(){ return Date.parse('today').moveToFirstDayOfMonth();  }, dateEnd: 'today' },
		],
		earliestDate: Date.parse('-2years'),
		latestDate: Date.parse('+0years'),
		changeMonth: true,
		changeYear: true,
	});
});
