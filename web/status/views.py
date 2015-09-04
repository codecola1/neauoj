from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def submit(req):
    if req.method == 'GET':
        return render_to_response('problem_submit.html', context_instance=RequestContext(req))