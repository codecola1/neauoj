/**
 * Created by Code_Cola on 15/10/8.
 */
var key, problems = new Array(26), number, iii = 0;
$(document).ready(function () {
    key = 0;
    number = 0;
    judge_title();
    $('#addlist').removeAttr('disabled');
    $('.form_datetime').datetimepicker({
        weekStart: 1,
        todayBtn: 1,
        autoclose: 1,
        todayHighlight: 1,
        startView: 2,
        forceParse: 0,
        showMeridian: 1
    });
    $("[id^='tab']").click(function () {
        page = $(this).attr('id').match(/\d+/);
        $.getJSON("/contest/info/{{ type }}/" + page, function (ret) {
            $('#info' + page).html(ret['data']);
        });
    });
    $("#tab1").trigger("click");
    $("#addlist").click(function () {
        addProblemRow();
    });
    $('#addproblemlist').on('click', '#deletelist', function () {
        $('#addlist').removeAttr('disabled');
        var index = $(this).parent().parent().index() + 1;
        var i, t = key & (Math.pow(2, index) - 1);
        key >>= (index + 1);
        key <<= index;
        key |= t;
        for (i = index - 1; i < 25; i++) {
            problems[i] = problems[i + 1];
        }
        problems[i] = 0;
        number--;
        $(this).parent().parent().remove();
        set_ok();
        test();
    });
    $('#addproblemlist').on('change', '[name=oj]', function () {
        updateProblemInfo($(this).parent().parent());
    });
});
function test() {
    //$('#test').html('key: ' + key.toString(2) + '<br>problems: ' + problems + '<br>number: ' + number + '<br> iii: ' + iii);
    //alert(key.toString(2));
    //alert(problems);
}
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
    test();
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
            if (data['index'] == iii) {
                if (data['pid']) {//alert('test');
                    if (problems[index]) {
                        var pt = problems[index];
                        problems[index] = data['pid'];
                        if (how_many(pt, problems) == 1) {
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
                    }
                    if (!(key & t)) {
                        key += t;
                    }
                    set_error();
                    $("[name=pid]", row).parent().addClass('has-error');
                    $("[name=title]", row).removeAttr('placeholder');
                }
            }
            test();
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
    newRow = Row.clone();
    $("[name=oj]", newRow).val($("[name=oj]", Row).val());
    $("[name=title]", newRow).val("");

    newRow.removeAttr("id");

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
}
