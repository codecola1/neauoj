/**
 * Created by Code_Cola on 15/11/18.
 */
var abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
var status_list_num = 0;
$(document).ready(function () {
    $("[id^='tab']").click(function () {
        var pid = $(this).attr('id').match(/\d+/);
        var cid = $('#cid').html();
        $('#id_problem').attr('value', pid);
        $.getJSON("/contest/problem/" + cid + "/" + pid, function (ret) {
            $('#title' + pid).html(abc[pid] + " - " + ret['title']);
            $('#tlc' + pid).html(ret['tlc']);
            $('#tlj' + pid).html(ret['tlj']);
            $('#mlc' + pid).html(ret['mlc']);
            $('#mlj' + pid).html(ret['mlj']);
            if (ret['description']) {
                var description = $('#description' + pid);
                description.parent().parent().removeAttr('hidden');
                description.html(ret['description']);
            }
            if (ret['input']) {
                var input = $('#input' + pid);
                input.parent().parent().removeAttr('hidden');
                input.html(ret['input']);
            }
            if (ret['output']) {
                var output = $('#output' + pid);
                output.parent().parent().removeAttr('hidden');
                output.html(ret['output']);
            }
            if (ret['sinput']) {
                var sinput = $('#sinput' + pid);
                sinput.parent().parent().removeAttr('hidden');
                sinput.html(ret['sinput']);
            }
            if (ret['soutput']) {
                var soutput = $('#soutput' + pid);
                soutput.parent().parent().removeAttr('hidden');
                soutput.html(ret['soutput']);
            }
            if (ret['hint']) {
                var hint = $('#hint' + pid);
                hint.parent().parent().parent().removeAttr('hidden');
                hint.html(ret['hint']);
            }
            if (ret['source']) {
                var source = $('#source' + pid);
                source.parent().parent().removeAttr('hidden');
                source.html(ret['source']);
            }
        });
    });
    $("#tab0").trigger("click");

    $("#status-tab").click(function () {
        var cid = $('#cid').html();
        $.getJSON("/contest/status/" + cid + "/1", function (ret) {
            make_status(1, ret);
        });
    });
    $("#status-previous").click(function () {
        var page = parseInt($("[id^='status_page'].active a").html()) - 1;
        $("#status_page" + page).trigger("click");
    });
    $("#status-next").click(function () {
        var page = parseInt($("[id^='status_page'].active a").html()) + 1;
        $("#status_page" + page).trigger("click");
    });
    $("#information-tab").click(function () {
        var cid = $('#cid').html();
        $.getJSON("/contest/info/" + cid, function (ret) {
            for (var i in ret) {
                if (ret[i][0] == 0) {
                    $("#problem_ac" + i).html("<span class='glyphicon glyphicon-remove' aria-hidden='true' style='color: #CC0000'></span>");
                }
                if (ret[i][0] == 1) {
                    $("#problem_ac" + i).html("<span class='glyphicon glyphicon-ok' aria-hidden='true' style='color: #00CC00'></span>");
                }
                $("#problem_submit" + i).html(ret[i][1]);
                $("#problem_solve" + i).html(ret[i][2]);
            }
        });
    });
});
$(document).on("click", "[id^='status_page']", function () {
    var page = $("a", this).html();
    var cid = $('#cid').html();
    $.getJSON("/contest/status/" + cid + "/" + page, function (ret) {
        make_status(page, ret);
    });
});
$(document).on("click", ".status-problem_id a", function () {
    var pid = $(this).html().charCodeAt(0) - 65;
    $("#problem-tab").trigger("click");
    $("#tab" + pid).trigger("click");
});
$(document).on("click", ".status-length a", function () {
    var cid = $('#cid').html();
    var rid = $(".status-row", $(this).parent().parent()).html();
    $("#statusModal .modal-title").html("Show Your Code - " + rid);
    $.getJSON("/contest/code/" + cid + "/" + rid, function (ret) {
        $("#statusModal .modal-body").html("<pre>" + ret['data'] + "</pre>");
    });
});
$(document).on("click", ".status-judge_status a", function () {
    var rid = $(".status-row", $(this).parent().parent()).html();
    $("#statusModal .modal-title").html("Compilation Error - Information - " + rid);
    $.getJSON("/status/ce_json/" + rid, function (ret) {
        $("#statusModal .modal-body").html("<pre>" + ret['data'] + "</pre>");
    });
});
function make_status(page, data) {
    var max_page = data['len'];
    var Row;
    while (status_list_num < max_page) {
        if (status_list_num) {
            Row = $("#status_list_exp").prev();
        }
        else {
            Row = $("#status_list_exp");
        }
        var newRow = Row.clone();
        var lid = $("a", newRow);
        if (lid.html().match(/^\s*\d+\s*$/)) {
            lid.html(parseInt(lid.html()) + 1);
        } else {
            lid.html("1");
        }
        newRow.attr("id", "status_page" + lid.html());
        //lid.attr("id", "status_page1");
        lid.removeAttr("hidden");
        newRow.insertBefore("#status_list_exp").show();
        status_list_num++;
    }
    $("[id^='status_page'].active").removeClass("active");
    var list_row = $("#status_list ul li:eq(" + page + ")");
    list_row.addClass("active");
    if (data['first']) {
        $("#status-previous").parent().removeClass("disabled");
    }
    else {
        $("#status-previous").parent().addClass("disabled");
    }
    if (data['last']) {
        $("#status-next").parent().removeClass("disabled");
    }
    else {
        $("#status-next").parent().addClass("disabled");
    }

    var exp_row = $("#status_exp");
    $("tr", exp_row.parent()).not("#status_exp").remove("");
    var status = data['status'];
    for (var i in status) {
        var new_row = exp_row.clone();
        new_row.removeAttr("hidden");
        new_row.removeAttr("id");
        $(".status-row", new_row).html(status[i][0]);
        var submit_time = new Date(status[i][1]);
        $(".status-submit_time", new_row).html(submit_time.getFullYear() + "年" + (submit_time.getMonth() + 1) + "月" + submit_time.getDate() + "日 " + (submit_time.getHours() < 10 ? "0" : "") + submit_time.getHours() + ":" + (submit_time.getMinutes() < 10 ? "0" : "") + submit_time.getMinutes());
        if (status[i][2] == 'Compilation Error') {
            $(".status-judge_status", new_row).html("<a href='javascript:void(0);' data-toggle='modal' data-target='#statusModal'>" + status[i][2] + "</a>");
        }
        else {
            $(".status-judge_status", new_row).html(status[i][2]);
        }
        $(".status-problem_id a", new_row).html(abc[status[i][3]]);
        $(".status-time", new_row).html(status[i][4]);
        $(".status-memory", new_row).html(status[i][5]);
        if (status[i][9]) {
            $(".status-length", new_row).html("<a href='javascript:void(0);' data-toggle='modal' data-target='#statusModal'>" + status[i][6] + "</a>");
        }
        else {
            $(".status-length", new_row).html(status[i][6]);
        }
        $(".status-language", new_row).html(status[i][7]);
        var user = $(".status-user a", new_row);
        user.html(status[i][8]);
        user.attr('href', '/accounts/userpage/' + status[i][8]);
        new_row.insertBefore("#status_exp").show();
    }
    $("#status-tab tbody tr").not("#status_exp").each(function () {
        up_color(this);
    });
    auto_refresh();
}
function up_color(Row) {
    var color = {
        'Accepte': '#CC0000',
        'Wrong A': '#00CC00',
        'Present': '#0000CC',
        'Compila': '#337AB7',
        'Time Li': '#FF6600',
        'Memory ': '#FF6600',
        'Runtime': '#FF6600'
    };
    var status = $(".status-judge_status", Row);
    status.attr("style", "color:" + color[status.html().substr(0, 7)]);
}
function auto_refresh() {
    $("#status-tab tbody tr").not("#status_exp").each(function () {
        //alert($(this).html());
        var status = $(".status-judge_status", this).html();
        var sid = $(".status-row", this).html();
        if (status.indexOf('Judging') != -1 || status.indexOf('Queuing') != -1 || status.indexOf('Compiling') != -1 || status.indexOf('Running') != -1) {
            fresh_result(sid, this);
        }
    });
}
function fresh_result(solution_id, row) {
    var url = "/status/get_status/" + solution_id + "/";
    $.getJSON(url, function (ret) {
        $(".status-judge_status", row).html(ret['status']);
        $(".status-time", row).html(ret['time']);
        $(".status-memory", row).html(ret['memory']);
        if (ret['status'] == "Judging" || ret['status'] == "Queuing" || ret['status'] == "Compiling" || ret['status'] == "Running") {
            window.setTimeout(function () {
                fresh_result(solution_id, row);
            }, 1000);
        }
        else {
            if (ret['status'] == 'Compilation Error') {
                $(".status-judge_status", row).html("<a href='javascript:void(0);' data-toggle='modal' data-target='#myModal'>Compilation Error</a>");
            }
            up_color(row);
        }
    });
}
/*
<span class='glyphicon glyphicon-ok' aria-hidden='true' style='color: #00CC00'></span>
<span class='glyphicon glyphicon-remove' aria-hidden='true' style='color: #CC0000'></span>
 */