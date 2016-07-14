from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from models import Problem
from forms import Add_problem_form, testform
from django.db.models import Q
from web.connect import Connect
from time import sleep

# Create your views here.


def problem_main(req, pid):
    if req.method == 'GET':
        try:
            p = Problem.objects.get(id=pid)
        except:
            return render_to_response('problem_error.html')
        wait = True
        if p.judge_type == 1:
            if p.defunct <= 0:
                c = Connect()
                c.download_problem(p.oj, p.problem_id, p.id)
            else:
                wait = False
                p.defunct = p.defunct - 1
                p.save()
        return render_to_response('problem_main.html', {
            'path': req.path,
            'p': p,
            'wait': wait
        }, context_instance=RequestContext(req))


@permission_required('problem.add_problem')
def add_problem(req):
    if req.method == 'POST':
        form = Add_problem_form(req.POST)
        if form.is_valid():
            new_problem = form.save()
            return HttpResponseRedirect("/")
        else:
            return render_to_response("add_problem.html", {
                'form': form,
            }, context_instance=RequestContext(req))
    else:
        form = Add_problem_form()
        return render_to_response('add_problem.html', {
            'form': form,
        }, context_instance=RequestContext(req))


@permission_required('problem.add_problem')
def test(req):
    p = None
    if req.method == 'POST':
        wait = True
        form = testform(req.POST)
        if form.is_valid():
            ind = form.cleaned_data['ind']
            oj = form.cleaned_data['oj']
            try:
                p = Problem.objects.get(oj=oj, problem_id=ind)
            except:
                p = Problem(oj=oj, problem_id=ind, judge_type=1)
                p.save()
                c = Connect()
                c.download_problem(oj, ind, p.id)
            else:
                if p.defunct <= 0:
                    c = Connect()
                    c.download_problem(oj, ind, p.id)
                else:
                    wait = False
        return render_to_response('problem_test.html', {
            'form': form,
            'path': req.path,
            'wait': wait,
            'p': p,
        }, context_instance=RequestContext(req))
    else:
        form = testform()
        return render_to_response('problem_test.html', {
            'form': form,
            'path': req.path,
            'wait': True,
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
        raise Http404()
    leng = len(pinfo)
    leng = leng / 20 if leng / 20. == leng // 20 else leng / 20 + 1
    return render_to_response('problem_list.html', {
        'path': req.path,
        'type': type,
        'len': range(leng),
    }, context_instance=RequestContext(req))

def get_problem(req, pid):
    data = {
        'wait': 1
    }
    try:
        p = Problem.objects.get(id=pid)
    except:
        raise Http404()
    if p.defunct <= 0:
        c = Connect()
        c.download_problem(p.oj, p.problem_id, p.id)
    else:
        data = {
            'wait': 0
        }
    return JsonResponse(data)

def get_problem_info(req, oj, problem_id, index):
    problem_id = int(problem_id)
    new = 0
    pinfo = ''
    data = {
        'pid': 0,
        'title': '',
        'index': index,
        'new': 0,
    }
    try:
        pinfo = Problem.objects.get(oj=oj, problem_id=problem_id)
    except:
        if oj != 'neau':
            # p = Problem(oj=oj, problem_id=problem_id, judge_type=1)
            # p.save()
            # c = Connect()
            # c.download_problem(oj, problem_id, p.id)
            # sleep(0.5)
            try:
                pinfo = Problem.objects.get(oj=oj, problem_id=problem_id)
            except:
                pinfo = ''
            else:
                new = 1
        else:
            pinfo = ''
    if pinfo:
        data = {
            'pid': pinfo.id,
            'title': pinfo.title,
            'index': index,
            'new': new
        }
    return JsonResponse(data)


def get_problem_list(req, type, page):
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
        pinfo = Problem.objects.filter(judge_type=0)
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
