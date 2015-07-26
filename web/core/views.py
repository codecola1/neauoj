from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

# Create your views here.

def index(req):
    k = False
    if req.user.is_authenticated():
        k = True
    if req.method == 'GET':

        return render_to_response('index.html', {
            "k":k
        }, context_instance=RequestContext(req))