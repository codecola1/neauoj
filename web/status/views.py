from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import SubmitForm
from models import Solve, ce_info
from users.models import User
from problem.models import Problem
import socket
import logging


# Create your views here.

logger = logging.getLogger(__name__)


@login_required
def submit(req):
    if req.method == 'GET':
        form = SubmitForm()
        return render_to_response('problem_submit.html', {
            'path': req.path,
            'form': form
        }, context_instance=RequestContext(req))
    if req.method == 'POST':
        form = SubmitForm(req.POST)
        form.set_user(req.user)
        form.set_contest(req.POST.get('contest', -1))
        if form.is_valid():
            new_submit = form.save()
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.connect("/tmp/neauoj.sock")
            client.send("0 " + str(new_submit.id) + " 0")
            receive = client.recv(1024)
            client.close()
            logger.info(receive)
            logger.info(u"User: " + req.user.username + u" Submited Problem: <" + new_submit.problem.oj + str(
                new_submit.problem.problem_id) + u"> Title: " + new_submit.problem.title)
            if form.contest_id >= 0:
                return HttpResponseRedirect("/contest/c/" + str(form.contest_id))  # + "?status=1"
            return HttpResponseRedirect("/status")
        else:
            return render_to_response("problem_submit.html", {
                'path': req.path,
                'form': form,
            }, context_instance=RequestContext(req))


@login_required
def rejudge(req, sid):
    if req.method == 'GET':
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect("/tmp/neauoj.sock")
        client.send(str(sid) + " 1")
        receive = client.recv(1024)
        client.close()
        logger.info(receive)
        logger.info(u"User: " + req.user.username + u" Rejudge Solve ID: <" + sid + u">")
        return HttpResponseRedirect("/status")
    raise Http404()


def ce(req, sid):
    if req.method == 'GET':
        try:
            s = Solve.objects.get(id=sid)
            c = ce_info.objects.get(solve=s)
        except:
            return render_to_response("problem_ce_info_error.html")
        return render_to_response("problem_ce_info.html", {
            'path': req.path,
            'info': c.info
        }, context_instance=RequestContext(req))


def ce_json(req, sid):
    if req.method == 'GET':
        try:
            s = Solve.objects.get(id=sid)
            c = ce_info.objects.get(solve=s)
        except:
            raise Http404()
        return JsonResponse({'data': c.info})


def status(req):
    if req.method == 'GET':
        page = int(req.GET.get('page', 1))
        all_solve = Solve.objects.order_by('-submit_time')
        l = len(all_solve)
        if page < 1 or page > l / 20 + 1:
            error = 1
            s = ''
        else:
            error = 0
            s = all_solve[(page - 1) * 20:page * 20]
        return render_to_response("status.html", {
            'error': error,
            'page': page,
            'path': req.path,
            'data': s,
            'over': 0 if page <= l / 20 else 1,
        }, context_instance=RequestContext(req))


def get_status(req, sid):
    try:
        s = Solve.objects.get(id=sid)
        data = {
            'status': s.status,
            'time': s.use_time,
            'memory': s.use_memory,
        }
    except:
        data = {}
    return JsonResponse(data)


def get_problem_status(req, uid, oj, problem_id, page):
    try:
        u = User.objects.get(id=uid)
        p = Problem.objects.get(oj=oj, problem_id=problem_id)
        s = Solve.objects.filter(user=u, problem=p).order_by('-submit_time')
    except:
        raise Http404()
    else:
        data = {
            'data': [],
            'previous': 0,
            'next': 0
        }
        f = lambda x: (
        x.id, x.submit_time, x.status, x.use_time, x.use_memory, len(x.code), x.language, 1 if req.user == u else 0)
        if page != '0':
            direction = int(page[-1])
            last_rid = int(page[:-1])
            num = 0
            k = 0
            if direction:
                for i in s:
                    num += 1
                    if k:
                        k += 1
                        data['data'].append(f(i))
                    if k == 11:
                        break
                    if i.id == last_rid:
                        k = 1
                data['previous'] = 1
                data['next'] = 0 if num == len(s) else 1
            else:
                for i in reversed(s):
                    num += 1
                    if k:
                        k += 1
                        data['data'].insert(0, f(i))
                    if k == 11:
                        break
                    if i.id == last_rid:
                        k = 1
                data['previous'] = 0 if num == len(s) else 1
                data['next'] = 1
        else:
            l = len(s) > 10
            for i in range(10 if l else len(s)):
                data['data'].append(f(s[i]))
            data['next'] = 1 if l else 0
    return JsonResponse(data)


@login_required
def show_code(req, sid):
    try:
        s = Solve.objects.get(id=sid)
        error = 0
        code = s.code
        if s.user != req.user and not req.user.has_perm('change_solve'):
            error = 2
    except:
        error = 1
        s = ''
        code = ''
    return render_to_response("show_code.html", {
        'path': req.path,
        'error': error,
        's': s,
        'code': code
    }, context_instance=RequestContext(req))
