from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from forms import SubmitForm


# Create your views here.

@login_required
def submit(req):
    if req.method == 'GET':
        form = SubmitForm()
        return render_to_response('problem_submit.html', {
            'form' : form
        }, context_instance=RequestContext(req))