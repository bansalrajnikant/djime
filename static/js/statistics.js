$(document).ready(function () {
  $('#from-to-date').datepicker({
    dateFormat: 'yy-mm-dd',
    rangeSelect: true,
    firstDay: 1,
    numberOfMonths: 2,
    maxDate: '1d'
  });
});
