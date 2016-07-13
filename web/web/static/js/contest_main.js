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
            $('#title' + pid).html(abc[pid] + ". " + ret['title']);
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
                    $("#problem_ac" + i).html("<span class='glyphicon glyphicon-ok' aria-hidden='true' style='color: #009900'></span>");
                }
                $("#problem_submit" + i).html(ret[i][1]);
                $("#problem_solve" + i).html(ret[i][2]);
            }
            $("#server_time").html(ret['time']);
            var contest_status = $("#ended");
            if (ret['status'] == 1) {
                contest_status.html("Ended");
            }
            else if (ret['status'] == -1) {
                contest_status.attr("style", "color:#9900CC");
                contest_status.html("Waiting");
            }
            else {
                contest_status.attr("style", "color:#3366FF");
                contest_status.html("Running");
            }
        });
    });
    $("#rank-tab").click(function () {
        var cid = $('#cid').html();
        $.getJSON("/contest/rank/" + cid, function (ret) {
            var user_key = {
                0: 0
            };
            var users = new Array();
            for (var i in ret['data']) {
                var info = ret['data'][i];
                if (info[3] > ret['end']) {
                    break;
                }
                if (!user_key[info[0]]) {
                    users.push(new User(info[0], ret['fb'].length));
                    user_key[info[0]] = user_key[0] + 1;
                    user_key[0]++;
                }
                if (info[2]) {
                    users[user_key[info[0]] - 1].problems[info[1]].ac = 1;
                    users[user_key[info[0]] - 1].problems[info[1]].use_time += info[3];
                    users[user_key[info[0]] - 1].all_time += users[user_key[info[0]] - 1].problems[info[1]].use_time;
                    users[user_key[info[0]] - 1].ac_num++;
                }
                else {
                    users[user_key[info[0]] - 1].problems[info[1]].penalty++;
                    users[user_key[info[0]] - 1].problems[info[1]].use_time += 1200;
                }
            }
            users.sort(function (a, b) {
                if (a.ac_num == b.ac_num) {
                    return a.all_time - b.all_time;
                }
                return b.ac_num - a.ac_num;
            });
            var Row;
            var exp_row = $("#rank_exp");
            $("tr", exp_row.parent()).not("#rank_exp").remove("");
            for (var i in users) {
                Row = exp_row;
                var newRow = Row.clone();
                $(".rank-row", newRow).html(parseInt(i) + 1);
                $(".rank-user", newRow).html(ret['user'][users[i].user_id][0] + "(" + ret['user'][users[i].user_id][1] + ")");
                $(".rank-solve", newRow).html(users[i].ac_num);
                $(".rank-total", newRow).html(parseInt(users[i].all_time / 60));
                for (var j in users[i].problems) {
                    if (users[i].problems[j].ac) {
                        $(".ac_time" + j, newRow).html(to_time(users[i].problems[j].use_time));
                        if (users[i].problems[j].penalty) {
                            $(".penalty" + j, newRow).html("(-" + users[i].problems[j].penalty + ")");
                        }
                        if (ret['fb'][j] == users[i].user_id) {
                            $(".rank_problem" + j, newRow).attr("style", "background-color: #007F00");
                        }
                        else {
                            $(".rank_problem" + j, newRow).attr("style", "background-color: #66FF66");
                        }
                    }
                    else if (users[i].problems[j].penalty) {
                        $(".penalty" + j, newRow).html("(-" + users[i].problems[j].penalty + ")");
                        $(".rank_problem" + j, newRow).attr("style", "background-color: #FF3333");
                    }
                }
                newRow.removeAttr("id");
                newRow.removeAttr("hidden");
                newRow.insertBefore(Row).show();
            }
        });
    });
    function One_problem(use_time, penalty) {
        this.use_time = use_time;
        this.penalty = penalty;
        this.ac = 0;
    }
    function User(user_id, problem_num) {
        this.user_id = user_id;
        this.problems = new Array(problem_num);
        for (var i = 0; i < problem_num; i++) {
            this.problems[i] = new One_problem(0, 0);
        }
        this.ac_num = 0;
        this.all_time = 0;
    }
    function to_time(time_s) {
        var s = time_s % 60;
        time_s = parseInt(time_s / 60);
        var m = time_s % 60;
        var h = parseInt(time_s / 60);
        return h + ":" + (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
    }
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
    $("#statusModal .modal-title").html("Show Code - " + rid);
    $.getJSON("/contest/code/" + cid + "/" + rid, function (ret) {
        $("#statusModal .modal-body").html('<pre class="prettyprint linenums">' + ret['data'] + "</pre>");
        prettyPrint();
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
        if (judging(status[i][2])) {
            $(".status-judging", new_row).html('<img src="/img/loading.gif" width="100%">');
        }
        else {
            $(".status-judging", new_row).html('');
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
        'Accepted': '#CC0000',
        'Wrong An': '#009900',
        'Presenta': '#0000CC',
        'Compilat': '#337AB7',
        'Time Lim': '#FF6600',
        'Memory L': '#FF6600',
        'Runtime ': '#FF6600',
        'Output L': '#FF6600'
    };
    var status = $(".status-judge_status", Row);
    status.attr("style", "color:" + color[status.html().substr(0, 8)]);
}
function auto_refresh() {
    $("#status-tab tbody tr").not("#status_exp").each(function () {
        //alert($(this).html());
        var status = $(".status-judge_status", this).html();
        var sid = $(".status-row", this).html();
        if (judging(status)) {
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
        if (judging(ret['status'])) {
            window.setTimeout(function () {
                fresh_result(solution_id, row);
            }, 1000);
        }
        else {
            if (ret['status'] == 'Compilation Error') {
                $(".status-judge_status", row).html("<a href='javascript:void(0);' data-toggle='modal' data-target='#statusModal'>Compilation Error</a>");
            }
            up_color(row);
            $(".status-judging", row).html('');
        }
    });
}
function judging(status) {
    return status.indexOf('Judging') != -1 || status.indexOf('Queuing') != -1 || status.indexOf('Compiling') != -1 || status.indexOf('Running') != -1;
}