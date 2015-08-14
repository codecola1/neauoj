from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

# Create your views here.


def problem_main(req, pid):
    if req.method == 'GET':
        return render_to_response('problem_main.html', {
        }, context_instance=RequestContext(req))