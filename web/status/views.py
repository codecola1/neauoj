from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import SubmitForm
from core.support.log_web import Log
from models import Solve, ce_info
import socket


# Create your views here.

logging = Log()


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
            logging.info(receive)
            logging.info(u"User: " + req.user.username + u" Submited Problem: <" + new_submit.problem.oj + str(
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
            'info': c.info
        }, context_instance=RequestContext(req))

def status(req):
    if req.method == 'GET':
        s = Solve.objects.order_by('-id')[0:20]
        return render_to_response("status.html", {
            'data': s
        }, context_instance=RequestContext(req))