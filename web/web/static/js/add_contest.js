/**
 * Created by Code_Cola on 15/10/8.
 */
var key, problems = new Array(26), titles = new Array(26), number, iii = 0;
$(document).ready(function () {
    key = 0;
    number = 0;
    set_error();
    judge_title();
    judge_start_time();
    judge_end_time();
    $('#addlist').removeAttr('disabled');
    $('.form_datetime').datetimepicker({
        weekStart: 1,
        //todayBtn: 1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        //showMeridian: 1,
        forceParse: 0
    });
    $("#addlist").click(function () {
        addProblemRow();
    });
    $('#addproblemlist').on('click', '#deletelist', function () {
        $('#addlist').removeAttr('disabled');
        var index = $(this).parent().parent().index() + 1;
        var i, t = key & (Math.pow(2, index) - 1), pt = problems[index - 1];
        key >>= (index + 1);
        key <<= index;
        key |= t;
        for (i = index - 1; i < 25; i++) {
            problems[i] = problems[i + 1];
            titles[i] = titles[i + 1];
        }
        problems[i] = 0;
        titles[i] = '';
        number--;
        $(this).parent().parent().remove();
        if (how_many(pt, problems) == 1) {
            remove_error(pt);
        }
        set_ok();
        make_data();
    });
    $('#addproblemlist').on('change', '[name=oj]', function () {
        updateProblemInfo($(this).parent().parent());
    });
    $("#id_start_time").change(function () {
        judge_start_time();
        judge_end_time();
    });
    $("#id_end_time").change(function () {
        judge_start_time();
        judge_end_time();
    });
});
function how_many(val, arr) {
    var cont = 0;
    for (var i = 0; i < 26; i++) {
        if (arr[i] == val) {
            cont++;
        }
    }
    return cont;
}
function set_error() {
    var b = $("#submit");
    b.attr('disabled', 'true');
    b.html('Error Info!');
}
function set_ok() {
    if (key || !number) {
        return;
    }
    var b = $("#submit");
    b.removeAttr('disabled');
    b.html('Submit');
}
function judge_title() {
    var title = $('#id_title');
    if (title.val().length) {
        if (key & 1) {
            key--;
        }
        set_ok();
        title.parent().removeClass('has-error');
    }
    else if (!(key & 1)) {
        key++;
        set_error();
        title.parent().addClass('has-error');
    }
}
function remove_error(pt) {
    for (var i = 0; i < 26; i++) {
        if (problems[i] == pt) {
            var tt = Math.pow(2, i + 1);
            if (key & tt) {
                key -= tt;
            }
            set_ok();
            $("[name=pid]", $("#all_list tr").eq(i + 1)).parent().removeClass('has-error');
            break;
        }
    }
}
function updateProblemInfo(row) {
    var oj = $("[name=oj]", row).val().toLocaleLowerCase();
    var pid = $("[name=pid]", row).val();
    if (!pid) {
        pid = 0;
    }
    iii++;
    $.ajax({
        type: "GET",
        url: "/problem/info/" + encodeURI(oj) + "/" + encodeURI(pid) + "/" + encodeURI(iii),
        dataType: "json",
        success: function (data) {
            var index = row.index();
            var t = Math.pow(2, index + 1);//alert(data['index'] == iii);
            if (data['index'] == iii || data['new']) {
                if (data['pid']) {//alert('test');
                    if (problems[index]) {
                        var pt = problems[index];
                        problems[index] = data['pid'];
                        if (how_many(pt, problems) == 1) {
                            remove_error(pt);
                        }
                    }
                    problems[index] = data['pid'];
                    var have = how_many(data['pid'], problems);
                    if (have > 1) {
                        for (var i = 0; i < 26; i++) {
                            if (problems[i] == data['pid']) {
                                var tt = Math.pow(2, i + 1);
                                if (!(key & tt)) {
                                    key += tt;
                                }
                                set_error();//alert($("[name=pid]", $("#all_list tr").eq(i)).parent().html());
                                $("[name=pid]", $("#all_list tr").eq(i + 1)).parent().addClass('has-error');
                            }
                        }
                    }
                    else {
                        if (key & t) {
                            key -= t;
                        }
                        set_ok();
                        $("[name=pid]", row).parent().removeClass('has-error');
                    }
                    $("[name=title]", row).attr('placeholder', data["title"]);
                } else {
                    if (problems[index]) {
                        var pt = problems[index];
                        problems[index] = data['pid'];
                        if (how_many(pt, problems) == 1) {
                            remove_error(pt);
                        }
                    }
                    if (!(key & t)) {
                        key += t;
                    }
                    set_error();
                    $("[name=pid]", row).parent().addClass('has-error');
                    $("[name=title]", row).removeAttr('placeholder');
                }
                make_data();
            }
        },
        error: function () {
            var index = row.index();
            var t = Math.pow(2, index + 1);
            if (!(key & t)) {
                key += t;
            }
            set_error();
            $("[name=pid]", row).parent().addClass('has-error');
        }
    });
}
function updateTitle(row) {
    var title = $("[name=title]", row).val();
    var index = row.index();
    titles[index] = title;
    make_data();
}
function judge_start_time() {
    var start_input = $('#id_start_time');
    var start_time = new Date(start_input.val().replace(/-/gm,'/'));
    start_time = start_time.getTime();
    var now = new Date();
    now = now.getTime();
    if (start_time > now) {
        start_input.parent().removeClass('has-error');
        if (key & 134217728) {
            key -= 134217728;
        }
        set_ok();
    }
    else {
        start_input.parent().addClass('has-error');
        if (!(key & 134217728)) {
            key += 134217728;
        }
        set_error();
    }
}
function judge_end_time() {
    var start_input = $('#id_start_time');
    var end_input = $('#id_end_time');
    var start_time = new Date(start_input.val().replace(/-/gm,'/'));
    start_time = start_time.getTime();
    var end_time = new Date(end_input.val().replace(/-/gm,'/'));
    end_time = end_time.getTime();
    var now = new Date();
    now = now.getTime();
    if (start_time && end_time > now && end_time > start_time) {
        end_input.parent().removeClass('has-error');
        if (key & 134217728) {
            key -= 134217728;
        }
        set_ok();
    }
    else {
        end_input.parent().addClass('has-error');
        if (!(key & 134217728)) {
            key += 134217728;
        }
        set_error();
    }
}
function addProblemRow() {
    var Row;
    if (number) {
        if (number >= 26) {
            $('#addlist').attr('disabled', 'true');
            return;
        }
        Row = $("#tr_exp").prev();
    } else {
        Row = $("#tr_exp");
    }
    var newRow = Row.clone();
    $("[name=oj]", newRow).val($("[name=oj]", Row).val());
    $("[name=title]", newRow).val("");

    newRow.removeAttr("id");
    $("[name=title]", newRow).removeAttr("placeholder");

    var pid = $("[name=pid]", newRow);
    if (pid.val().match(/^\s*\d+\s*$/)) {
        pid.val(parseInt(pid.val()) + 1);
    } else {
        pid.val("");
    }
    number++;
    newRow.insertBefore("tr#tr_exp").show();
    updateProblemInfo(newRow);
    if (number >= 26) {
        $('#addlist').attr('disabled', 'true');
    }
    make_data();
}
function make_data() {
    var data = {
        'number': number,
        'problems': problems,
        'titles': titles
    };
    $("#data").val(JSON.stringify(data));
}