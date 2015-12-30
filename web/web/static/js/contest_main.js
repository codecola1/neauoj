/**
 * Created by Code_Cola on 15/11/18.
 */
$(document).ready(function () {
    var abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
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
});