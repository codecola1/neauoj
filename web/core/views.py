from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User

# Create your views here.

def index(req):
    u = User.objects.get(username = 'tttt')
    i = u.info.nickname
    if req.method == 'GET':
        return render_to_response('index.html', {
            'str':i
        }, context_instance=RequestContext(req))