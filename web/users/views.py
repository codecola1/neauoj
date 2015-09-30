from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from users.forms import UserRegisterForm, PermissionForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.support.log_web import Log


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
                'path': req.path,
                'form': form,
            }, context_instance=RequestContext(req))
    else:
        form = UserRegisterForm()
        return render_to_response("register.html", {
            'path': req.path,
            'form': form,
        }, context_instance=RequestContext(req))


def index(req, username):
    try:
        user = User.objects.get(username=username)
    except:
        return render_to_response("user_error.html", {
            'path': req.path,
            'username': username,
        })
    return render_to_response("user_main.html", {
        'path': req.path,
        'u': user,
    }, context_instance=RequestContext(req))


@login_required
def account(req):
    return render_to_response("account.html", {
        'path': req.path,
    }, context_instance=RequestContext(req))


@permission_required('problem.add_permission')
def permission(req):
    users = User.objects.all()
    data = [(x.username, y.name) for x in users for y in x.user_permissions.all()]
    if req.method == 'GET':
        form = PermissionForm()
        return render_to_response("permission.html", {
            'form': form,
            'data': data
        }, context_instance=RequestContext(req))
    else:
        form = PermissionForm(req.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/accounts/permission")
        else:
            return render_to_response("permission.html", {
                'form': form,
                'data': data
            }, context_instance=RequestContext(req))