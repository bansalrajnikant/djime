/* JavaScript common to the entire Djime app. */

$(document).ready(function () {
    // Message sendt from django auth messaging.
    $("#content #messages li")
    // Add a close button
    .prepend('<span class="close">&times;</span>')
    // Rounded corners
    .corner()
    // And hide it on click
    .click(function () {
        $(this).fadeOut()
    });
	var container = $("#id_project").parent()
	$("#id_project").autocomplete(djime.autocomplete_projectnames);
	$("#id_project").keyup(function () {
		var i=0;
		while (djime.autocomplete_projectnames[i]) {
			if (String($("#id_project").val()) == djime.autocomplete_projectnames[i][0]) {
				$("#id_client").val(djime.autocomplete_projectnames[i][1]);
			}
			i=i+1
		}
	});
	$("#id_client").mouseup(function () {
		if (isNaN(parseInt($(this).val())) == false) {
			if (djime.client_list[parseInt($("#id_client").val())] == 0) {
				$("#id_project").val('');
				container.hide();
			}
			else {
				container.show();
				$("#id_project").remove();
				container.append('<select id="id_project" name="project">' + djime.client_list[parseInt($("#id_client").val())] + '</select>');
			}
		}
		else {
			container.show();
			$("#id_project").remove();
			container.append('<input type="text" id="id_project" name="project" autocomplete="off" class="ac_input"/>');
			$("#id_project").autocomplete(djime.autocomplete_projectnames);
		}
	});
});

