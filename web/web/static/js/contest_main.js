/**
 * Created by Code_Cola on 15/11/18.
 */
$(document).ready(function () {
    var abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    var status_list_num = 0;
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
            var max_page = ret['len'];
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
});
$(document).on("click", "[id^='status_page']", function () {
    var page = $("a", this).html();
    var cid = $('#cid').html();
    $.getJSON("/contest/status/" + cid + "/" + page, function (ret) {
        make_status(page, ret);
    });
});
function make_status(page, data) {
    $("[id^='status_page'].active").removeClass("active");
    var Row = $("#status_list ul li:eq(" + page + ")");
    Row.addClass("active");
    //if (ret['description']) {
    //    var description = $('#description' + pid);
    //    description.parent().parent().removeAttr('hidden');
    //    description.html(ret['description']);
    //}

    //if (!status_list_num) {
    //    newRow.addClass("active");
    //}
}