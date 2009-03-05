$(document).ready(function () {
  $('#id_date').datepicker({
    dateFormat: 'yy-mm-dd',
    rangeSelect: true,
    firstDay: 1,
    numberOfMonths: 2,
    maxDate: '1d'
  });
	$('#billing-date').datepicker({
    dateFormat: 'yy-mm-dd',
    firstDay: 1,
    maxDate: '1d'
	});
});
