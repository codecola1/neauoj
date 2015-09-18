from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from models import Contest

# Create your views here.

def contest_list(req):
    if req.path[9] == 'a':
        cinfo = Contest.objects.filter(type=0)
        type = 'ACM'
    elif req.path[9] == 's':
        cinfo = Contest.objects.filter(type=1)
        type = 'Student'
    else:
        cinfo = Contest.objects.filter(type=3)
        type = 'VJudge'
    return render_to_response('contest_list.html', {
        'type': type,
        'info': cinfo,
    }, context_instance=RequestContext(req))
