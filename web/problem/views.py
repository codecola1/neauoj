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
        pinfo = Problem.objects.filter(judge_type=0)
        type = 'ACM'
    elif req.path[9] == 's':
        pinfo = Problem.objects.filter(Q(judge_type=2) | Q(judge_type=3))
        type = 'Student'
    else:
        raise Http404
    return render_to_response('problem_list.html', {
        'type': type,
        'len': range(len(pinfo) / 20 + 1),
    }, context_instance=RequestContext(req))


def get_problem_info(req, type, page):
    data = {'test': '''
<tr>
    <th scope="row">1</th>
    <td>1000</td>
    <td><a href='/problem/p/%s'>A + B</a></td>
    <td>ACM Team</td>
    <td>NEAU</td>
    <td>0</td>
    <td>0</td>
</tr>
    ''' % "1"}
    return JsonResponse(data)