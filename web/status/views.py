from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import SubmitForm
from core.support.log_main import Log


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
            logging.info(u"User: " + req.user.username + u" Submited Problem: <" + new_submit.problem.oj + str(
                new_submit.problem.problem_id) + u"> Title: " + new_submit.problem.title)
            return HttpResponseRedirect("/index")
        else:
            return render_to_response("problem_submit.html", {
                'path': req.path,
                'form': form,
            }, context_instance=RequestContext(req))