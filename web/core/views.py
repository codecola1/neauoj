from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User

# Create your views here.

def index(req):
    if req.method == 'GET':
        return render_to_response('index.html', {
        }, context_instance=RequestContext(req))

def test(req):
    from robot.access import Access
    ac = Access(oj='hdu')
    html = ac.get_html(url='http://acm.hdu.edu.cn/showproblem.php?pid=1022')
    return render_to_response('test.html', {
        'html':html
    })