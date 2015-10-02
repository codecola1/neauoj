from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import SubmitForm
from models import Solve, ce_info
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
        if form.is_valid():
            new_submit = form.save()
            client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            client.connect("/tmp/judge.sock")
            client.send(str(new_submit.id))
            receive = client.recv(1024)
            client.close()
            logger.info(receive)
            logger.info(u"User: " + req.user.username + u" Submited Problem: <" + new_submit.problem.oj + str(
                new_submit.problem.problem_id) + u"> Title: " + new_submit.problem.title)
            return HttpResponseRedirect("/status")
        else:
            return render_to_response("problem_submit.html", {
                'path': req.path,
                'form': form,
            }, context_instance=RequestContext(req))


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


def status(req):
    if req.method == 'GET':
        page = int(req.GET.get('page', 1))
        all_solve = Solve.objects.order_by('-id')
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