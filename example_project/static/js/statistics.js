$(document).ready(function () {
  $('#id_date').datepicker({
    dateFormat: 'yy-mm-dd',
    rangeSelect: true,
    firstDay: 1,
    numberOfMonths: 2,
    maxDate: '1d'
  });
  $('#id_team_statistics_date_selection').datepicker({
    dateFormat: 'yy-mm-dd',
    rangeSelect: true,
    firstDay: 1,
    numberOfMonths: 2,
    maxDate: '1d'
  });
});
