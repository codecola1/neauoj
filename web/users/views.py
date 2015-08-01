from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from users.froms import UserRegisterForm
from django.contrib.auth.models import User

# Create your views here.

def register(req):
    if req.method == 'POST':
        form = UserRegisterForm(req.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/index")
        else:
            return render_to_response("register.html", {
                'form': form,
            }, context_instance=RequestContext(req))
    else:
        form = UserRegisterForm()
        return render_to_response("register.html", {
            'form': form,
        }, context_instance=RequestContext(req))

def index(req, username):
    try:
        user = User.objects.get(username = username)
    except:
        user = None
        find_error = True
    else:
        find_error = False
    return render_to_response("user_main.html", {
        'find_error' : find_error,
        'u' : user,
        'username' : username,
    }, context_instance=RequestContext(req))