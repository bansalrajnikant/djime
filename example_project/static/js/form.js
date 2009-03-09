$("#slip-add-form").hide();

$(document).ready(function () {
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
	})
	
	$("#create-slip-button").click(function () {
		var create_box = $("#slip-add-form");
		create_box.dialog("open");
	})
	
	project.change(function () {
		project.removeClass('ui-state-error');
		checkProject(project, project.val(), "Project does not exist.")
	})
	
	name.change(function () {
		name.removeClass('ui-state-error');
		checkName(name, name.val(), "This field is required.")
	})
});