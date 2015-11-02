from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.http import JsonResponse, Http404
from django.template import RequestContext
from models import Contest
from forms import AddContestForm
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.

def contest_main(req, cid):
    if req.method == 'GET':
        cinfo = Contest.objects.get(id=cid)
        return render_to_response('contest_main.html', {
            'path': req.path,
        }, context_instance=RequestContext(req))


@permission_required('contest.add_contest')
def add_contest(req, type):
    if type not in ['acm', 'student', 'vjudge'] or req.method == 'GET':
        raise Http404()
    if req.method == 'POST':
        form = AddContestForm()
        return render_to_response('contest_add.html', {
            'path': req.path,
            'form': form,
        }, context_instance=RequestContext(req))


def contest_list(req):
    if req.path[9:16] == 'acmlist':
        cinfo = Contest.objects.filter(type=0)
        type = 'ACM'
    elif req.path[9:20] == 'studentlist':
        cinfo = Contest.objects.filter(type=1)
        type = 'Student'
    elif req.path[9:19] == 'vjudgelist':
        cinfo = Contest.objects.filter(type=2)
        type = 'VJudge'
    else:
        raise Http404()
    leng = len(cinfo)
    leng = leng / 20 if leng / 20. == leng // 20 else leng / 20 + 1
    return render_to_response('contest_list.html', {
        'path': req.path,
        'type': type,
        'len': range(leng),
    }, context_instance=RequestContext(req))


def get_contest_info(req, type, page):
    page = int(page)
    first = (page - 1) * 20
    last = page * 20
    data = {'data': ''}
    html = '''
<tr>
    <th scope="row">%s</th>
    <td>%s</td>
    <td><a href='/problem/p/%s'>%s</a></td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
</tr>
'''
    if req.path[9] == 'a':
        cinfo = Contest.objects.filter(type=0)
    elif req.path[9] == 's':
        cinfo = Contest.objects.filter(type=1)
    else:
        cinfo = Contest.objects.filter(type=2)
    last = last if last < len(cinfo) else len(cinfo)
    cinfo = cinfo[first:last]
    ii = (page - 1) * 20 + 1
    for i in cinfo:
        s = html % (ii, i.id, i.title, i.start_time, i.end_time, i.length, "Private" if i.private else "Public")
        data['data'] += s
        ii += 1
    return JsonResponse(data)