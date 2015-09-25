from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.template import RequestContext
from models import Problem
from django.db.models import Q

# Create your views here.


def problem_main(req, pid):
    if req.method == 'GET':
        try:
            p = Problem.objects.get(id=pid)
        except:
            return render_to_response('problem_error.html')
        return render_to_response('problem_main.html', {
            'path': req.path,
            'p': p,
        }, context_instance=RequestContext(req))


def problem_list(req):
    if req.path[9] == 'a':
        pinfo = Problem.objects.filter(judge_type=1)
        type = 'ACM'
    elif req.path[9] == 's':
        pinfo = Problem.objects.filter(Q(judge_type=2) | Q(judge_type=3))
        type = 'Student'
    else:
        raise Http404
    return render_to_response('problem_list.html', {
        'path': req.path,
        'type': type,
        'len': range(len(pinfo) / 20 + 1),
    }, context_instance=RequestContext(req))


def get_problem_info(req, type, page):
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
    if type == 'ACM':
        pinfo = Problem.objects.filter(judge_type=1)
    elif type == 'Student':
        pinfo = Problem.objects.filter(Q(judge_type=2) | Q(judge_type=3))
    else:
        raise Http404
    last = last if last < len(pinfo) else len(pinfo)
    pinfo = pinfo[first:last]
    ii = (page - 1) * 20 + 1
    for i in pinfo:
        s = html % (ii, i.problem_id, i.id, i.title, i.source, i.oj, i.submit, i.solved)
        data['data'] += s
        ii += 1
    return JsonResponse(data)