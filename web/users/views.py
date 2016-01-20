from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from users.forms import UserRegisterForm, PermissionForm, ChangePasswd, AddUserForm, EditInforForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
import logging

from problem.models import Problem
from contest.models import Contest
from status.models import Solve

# Create your views here.


logger = logging.getLogger(__name__)


def register(req):
    if req.method == 'POST':
        form = UserRegisterForm(req.POST)
        if form.is_valid():
            new_user = form.save()
            logger.info("User: " + new_user.username + "Registered")
            return HttpResponseRedirect("/index")
        else:
            return render_to_response("register.html", {
                'path': req.path,
                'form': form,
            }, context_instance=RequestContext(req))
    else:
        form = UserRegisterForm()
        return render_to_response("register.html", {
            'path': '/',
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
    all_solve = Solve.objects.filter(user=user)
    return render_to_response("user_main.html", {
        'path': req.path,
        'u': user,
    }, context_instance=RequestContext(req))


@login_required
def account(req):
    return render_to_response("account.html", {
        'path': req.path,
    }, context_instance=RequestContext(req))


@login_required
def change_password(req):
    if req.method == 'GET':
        form = ChangePasswd()
        return render_to_response("change_password.html", {
            'form': form,
        }, context_instance=RequestContext(req))
    else:
        form = ChangePasswd(req.POST)
        form.set_user(req.user)
        if form.is_valid():
            form.save()
            referer = req.META['HTTP_REFERER']
            if referer[-20:] == '/accounts/useradmin/':
                return HttpResponseRedirect("/accounts/useradmin")
            return HttpResponseRedirect("/accounts/logout")
        else:
            return render_to_response("change_password.html", {
                'form': form,
            }, context_instance=RequestContext(req))


@login_required
def edit_information(req):
    if req.method == 'GET':
        form = EditInforForm()
        return render_to_response("edit_information.html", {
            'form': form,
        }, context_instance=RequestContext(req))
    else:
        form = EditInforForm(req.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/index")
        else:
            return render_to_response("edit_information.html", {
                'form': form,
            }, context_instance=RequestContext(req))


@permission_required('auth.add_permission')
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


@permission_required('auth.change_user')
def useradmin(req):
    users = User.objects.exclude(is_superuser='1')
    if req.method == 'GET':
        form = AddUserForm()
        page = int(req.GET.get('page', 1))
        return render_to_response("UserAdmin.html", {
            'form': form,
            'users': users[20 * (page - 1):20 * page],
            'length': range(1, len(users) / 20 + 2),
        }, context_instance=RequestContext(req))
    else:
        form = AddUserForm(req.POST)