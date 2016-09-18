/**
 * Created by Code_Cola on 15/10/5.
 */
var last_problem = "", thread;

$(document).ready(function(){
		$('#begin_time').datetimepicker({
			weekStart: 1,
			todayBtn:  1,
			autoclose: 1,
			todayHighlight: 1,
			startView: 2,
			forceParse: 0,
			showMeridian: 1
		});
		$('#end_time').datetimepicker({
			weekStart: 1,
			todayBtn:  1,
			autoclose: 1,
			todayHighlight: 1,
			startView: 2,
			forceParse: 0,
			showMeridian: 1
		});
		$('#freeze_time').datetimepicker({
			weekStart: 1,
			todayBtn:  1,
			autoclose: 1,
			todayHighlight: 1,
			startView: 2,
			forceParse: 0,
			showMeridian: 1
		});

		var upd_probs = '';
		$("#addProblemTable tr.tr_problem:visible").each(function(index){
			//updateProblemRow($(this));
			var pid = $("[name=pid]", $(this)).val();
			if (pid.length == 0) return;
			if (upd_probs != '') upd_probs += ',';
			upd_probs += pid;
		});

		$.ajax({
				type : "POST",
				url :  "?c=problem-pinfo2",
				data : {"problems" : upd_probs},
				dataType : "json",
				success: function(data, textStatus){
					$("#addProblemTable tr.tr_problem:visible").each(function(index){
						var row = $(this);
						var pid = $("[name=pid]", row).val();
						if (pid.length == 0) return;
						if (data.hasOwnProperty(pid)) {
							$("[name=pid]", row).val( data[pid]["id"] );
							$("[name=title]", row).val( data[pid]["title"] );
							row.children().eq(-1).html( '<a href="?c=problem-problem&id=' + data[pid]['id'] + '">' + data[pid]["title"] + '</a>' );
						}
					});
					updateProblemOrder();
				},
				error: function(XMLHttpRequest, textStatus, errorThrown){
			//		alert( JSON.stringify(XMLHttpRequest.responseText) );
				}
			});


		$("#addProblemBtn").click(function(){
			addProblemRow();
		});

		$('#addProblemTable').on('click', '.deleteProblemRow', function(){
			 $(this).parent().parent().remove();
			 updateProblemOrder();
		});

		$('#addProblemTable').on('change', '[name=OJ]', function(){
			updateProblemRow($(this).parent().parent());
		});

		$('#addProblemTable').on('focus', '[name=probNum]', function(){
			var row = $(this).parent().parent();
			last_problem = $("[name=OJ]", row).val() + ":" + $("[name=probNum]", row).val();
			thread = window.setInterval(function(){
						updateProblemRow(row);
						},
						1000 );
		});

		$('#addProblemTable').on('blur', '[name=probNum]', function(){
			var row = $(this).parent().parent();
			window.clearInterval(thread);
			updateProblemRow(row);
		});

		$("#formContest").submit(function(){
			$("#submitContest").attr("disabled", true);
			if ($('#contest_title').val().length == 0) {
				$('#contest_title').focus();
				alert('Contest title is required!');
				$("#submitContest").attr("disabled", false);
				return false;
			}
			if ($("#addProblemTable tr.tr_problem:visible").length < 1) {
				alert("Please add one problem at least!");
				$("#submitContest").attr("disabled", false);
				return false;
			}
			var rPid = /^[0-9]*[1-9][0-9]*$/;
			var dup = 0, err = 0, trs = $("#addProblemTable tr.tr_problem:visible");
			if (trs.length > 128) { // 鍗曚釜姣旇禌鏈€澶氱殑棰樼洰鏁伴噺
				alert("128 problems at most!\nPlease delete some problems.");
				$("#submitContest").attr("disabled", false);
				return false;
			}
			for (i = 0; i < trs.length; i++) {
				var pi = $("[name=pid]", trs.eq(i)).val();
				if (!rPid.test(pi)) {
					$("[name=probNum]", trs.eq(i)).focus();
					err = 1;
					break;
				}
				for (j = 0; j < i; j++) {
					if ($("[name=pid]", trs.eq(i)).val() == $("[name=pid]", trs.eq(j)).val()) {
						$("[name=probNum]", trs.eq(i)).focus();
						dup = 1;
						break;
					}
				}
			}
			if (err) {
				alert("There are invalid problems!");
				$("#submitContest").attr("disabled", false);
				return false;
			}
			if (dup) {
				alert("Duplcate problems are not allowed!");
				$("#submitContest").attr("disabled", false);
				return false;
			}
			updateProblemOrder();
			return true;
		});

});

function addProblemRow() {
	var originRow;
	if ($("#addProblemTable tr.tr_problem:visible").length){
		originRow = $("tr#addProblemRow").prev();
	} else {
		originRow = $("tr#addProblemRow");
	}
	newRow = originRow.clone();
	$("[name=OJ]", newRow).val($("[name=OJ]", originRow).val());
	$("[name=title]", newRow).val("");

	newRow.removeAttr("id");
	$(":input", newRow).removeAttr("id");

	var probNum = $("[name=probNum]", newRow);
	if (probNum.val().match(/^\s*\d+\s*$/)){
		probNum.val(parseInt(probNum.val()) + 1);
	} else {
		probNum.val("");
	}
	newRow.insertBefore("tr#addProblemRow").show();
	updateProblemRow(newRow);

}

function updateProblemRow(row) {
	var OJ = $("[name=OJ]", row);
	var probNum = $("[name=probNum]", row);
	var new_problem = OJ.val() + ":" + probNum.val();
	if (new_problem == last_problem) return;

	last_problem = new_problem;
	//alert( last_problem );
	$.ajax({
		type : "GET",
		url :  "?c=problem-pinfo&OJ=" + encodeURI(OJ.val()) + "&probNum=" + encodeURI(probNum.val()),
		dataType : "json",
		success: function(data, textStatus){
			//alert( JSON.stringify(data) );
			if (data["id"] != -1) {
				$("[name=pid]", row).val( data["id"] );
				$("[name=title]", row).val( data["title"] );
				row.children().eq(-1).html( '<a href="?c=problem-problem&id=' + data['id'] + '">' + data["title"] + '</a>' );
			} else {
				$("[name=pid]", row).val( "" );
				$("[name=title]", row).val( "" );
				row.children().eq(-1).html('<span class="label label-warning">No such problem!</span>');
			}
			updateProblemOrder();
		},
		error: function(XMLHttpRequest, textStatus, errorThrown){
			row.children().eq(-1).html('<span class="label label-warning">Get problem info error!</span>');
			//alert(textStatus);
		}
	});
}

function updateProblemOrder() {
	var problems = {};
	var idx = 0;
	$("#addProblemTable tr.tr_problem:visible").each(function(index){
		var pid = $("[name=pid]", this).val();
		if (pid.length > 0) {
			problems[idx] = {
				'problem_id' : pid,
				'title' : $("[name=title]", this).val()
			};
			idx++;
		}
	});
	$("#problems").val( JSON.stringify( problems ) );
}

