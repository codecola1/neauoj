from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from users.forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.support.log_main import Log


# Create your views here.

logging = Log()


def register(req):
    if req.method == 'POST':
        form = UserRegisterForm(req.POST)
        if form.is_valid():
            new_user = form.save()
            logging.info("User: " + new_user.username + "Registered")
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
        user = User.objects.get(username=username)
    except:
        return render_to_response("user_error.html", {
            'username': username,
        })
    return render_to_response("user_main.html", {
        'u': user,
    }, context_instance=RequestContext(req))


@login_required
def account(req):
    return render_to_response("account.html", {

    }, context_instance=RequestContext(req))