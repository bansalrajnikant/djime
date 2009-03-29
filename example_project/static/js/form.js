$("#slip-add-form").hide();

$.getJSON('/project/json/', function(data) {
		djime.autocomplete_projectnames = new Array();
		for (i = 0; i < data[0].length; i++) {
			djime.autocomplete_projectnames[i] = data[0][i]
		};
		djime.client_list = new Array();
		djime.client_list = data[1];
	});

$(document).ready(function () {
	var container = $("#id_project").parent();
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
				project = $("#id_project");
			}
		}
		else {
			container.show();
			$("#id_project").remove();
			container.append('<input type="text" id="id_project" name="project" autocomplete="off" class="ac_input"/>');
			$("#id_project").autocomplete(djime.autocomplete_projectnames);
			project = $("#id_project");
			$("#id_project").keyup(function () {
				var i=0;
				while (djime.autocomplete_projectnames[i]) {
					if (String($("#id_project").val()) == djime.autocomplete_projectnames[i][0]) {
						$("#id_client").val(djime.autocomplete_projectnames[i][1]);
					}
					i=i+1
				}
			});
		}
	});

	var name = $("#id_name"),
		project = $("#id_project"),
		client = $("#id_client"),
		allFields = $([]).add(name).add(project).add(client),
		tips = $("#validateTips");

	function updateTips(t) {
		tips.text(t).effect("highlight",{},1500);
	}

	function checkName(div,name,tip) {
		if (name == '') {
			div.addClass('ui-state-error');
			updateTips(tip);
			return false;
		}
		else {
			return true;
		}
	}

	function checkProject(div,project,tip) {
		var match = false;
		if (project == '') {
			match = true
		}
		for (i = 0; i < djime.autocomplete_projectnames.length; i++) {
			if (project.toLowerCase() == djime.autocomplete_projectnames[i][0].toLowerCase()) {
				match = true
			}
		}
		if (!(match)) {	
			div.addClass('ui-state-error');
			updateTips(tip);
			return false;
		}
		else {
			return true;
		}
	}

	$("#slip-add-form").dialog({
		bgiframe: true,
		autoOpen: false,
		height: 300,
		modal: true,
		buttons: {
			'Create task': function() {
				var bValid = true
				allFields.removeClass('ui-state-error');
				bValid = bValid && checkProject(project, project.val(), "Project does not exist.")
				bValid = bValid && checkName(name, name.val(), "This field is required")

				if (bValid) {
					$.post("/slip/add/", { 'name': name.val(), 'project': project.val(), 'client': client.val()},
						function(data){
							document.location.href = '/' + data
					});
					$(this).dialog("close");
				}
			},
			Cancel: function() {
				$(this).dialog('close');
			},
		},
		close: function() {
			allFields.val('').removeClass('ui-state-error');
		},		
	});
	
	$("#create-slip-button").click(function () {
		var create_box = $("#slip-add-form");
		create_box.dialog("open");
	});
	
	project.change(function () {
		project.removeClass('ui-state-error');
		tips.text('');
		checkProject(project, project.val(), "Project does not exist.");
	});
});