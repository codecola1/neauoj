from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User, Permission
from problem.robot.get_problem import Down_problem


# Create your views here.

def index(req):
    if req.method == 'GET':
        return render_to_response('index.html', {
            'path': req.path,
        }, context_instance=RequestContext(req))
