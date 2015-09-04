from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from models import Problem

# Create your views here.


def problem_main(req, pid):
    if req.method == 'GET':
        try:
            p = Problem.objects.get(id=pid)
        except:
            return render_to_response('problem_error.html')
        return render_to_response('problem_main.html', {
            'p': p,
        }, context_instance=RequestContext(req))
