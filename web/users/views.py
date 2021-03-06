from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.template import RequestContext
from users.forms import *
from users.models import OJ_account, submit_problem
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
import logging
import time
from web.connect import Connect

from status.models import Solve

# Create your views here.


logger = logging.getLogger(__name__)


def register(req):
    if req.method == 'POST':
        form = UserRegisterForm(req.POST)
        if form.is_valid():
            new_user = form.save()
            logger.info("User: " + new_user.username + "Registered")
            return HttpResponseRedirect("/")
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


def classify(l):
    data = {}
    for i in l:
        if i[0] not in data:
            data[i[0]] = []
        data[i[0]].append(i[1])
    for i in data:
        data[i].sort()
        data[i] = [data[i][x * 10: x * 10 + 10] for x in range(len(data[i]) / 10 + (1 if len(data[i]) % 10 else 0))]
    return data


def index(req, username):
    try:
        user = User.objects.get(username=username)
    except:
        return render_to_response("user_error.html", {
            'path': req.path,
            'username': username,
        })
    all_solve = Solve.objects.filter(user=user)
    submissions = len(all_solve)
    solved_info = {}
    problem_unsolved = []
    problem_solved = []
    data = submit_problem.objects.filter(user=user, ac=1)
    for i in data:
        problem_solved.append(i.problem.id)
        solved_info[i.problem.id] = [i.problem.oj, i.problem.problem_id]
    data = submit_problem.objects.filter(user=user, ac=0)
    for i in data:
        problem_unsolved.append(i.problem.id)
        solved_info[i.problem.id] = [i.problem.oj, i.problem.problem_id]
    problem_solved = set(problem_solved)
    problem_unsolved = list(set(problem_unsolved) - problem_solved)
    problem_solved = list(problem_solved)
    for i in range(len(problem_solved)):
        problem_solved[i] = solved_info[problem_solved[i]]
    for i in range(len(problem_unsolved)):
        problem_unsolved[i] = solved_info[problem_unsolved[i]]
    solved = len(problem_solved)
    problem_solved = classify(problem_solved)
    problem_unsolved = classify(problem_unsolved)
    now = time.time() - 2592000
    month_solve = []
    survey_date = []
    survey_solved = [0] * 30
    survey_submit = [0] * 30
    survey_key = {}
    for i in all_solve:
        submit_time = time.mktime(i.submit_time.timetuple())
        if now <= submit_time and time.time() > submit_time:
            month_solve.append(i)
    # month_solve.sort(key=lambda x: x.submit_time)
    now = time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime()), "%Y-%m-%d"))
    today = now
    yesterday = today - 86400
    for i in range(30)[::-1]:
        survey_date.insert(0, time.strftime("%d", time.localtime(today)))
        survey_key[time.strftime("%Y-%m-%d", time.localtime(today))] = i
        today = yesterday
        yesterday -= 86400
    for i in month_solve:
        survey_submit[survey_key[time.strftime("%Y-%m-%d", i.submit_time.timetuple())]] += 1
        if i.status == 'Accepted':
            try:
                f = Solve.objects.filter(user=user, problem=i.problem, status='Accepted').order_by('submit_time')[0]
            except:
                continue
            else:
                if f == i:
                    survey_solved[survey_key[time.strftime("%Y-%m-%d", i.submit_time.timetuple())]] += 1
    num_accounts = 0
    for i in user.info.oj_account.all():
        if not i.defunct:
            num_accounts += 1
    try:
        updata_user(user)
    except:
        pass
    return render_to_response("user_main.html", {
        'path': req.path,
        'u': user,
        'accounts': num_accounts,
        'num_solved': solved,
        'num_submissions': submissions,
        'solved': problem_solved,
        'unsolved': problem_unsolved,
        'survey_date': survey_date,
        'survey_solved': survey_solved,
        'survey_submit': survey_submit,
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


@login_required
def add_account(req):
    if req.method == 'GET':
        raise Http404()
    else:
        form = AccountForm(req.POST)
        if form.is_valid():
            data = form.save()
            ok = test_account(data[2], data[0], data[1])
            if not ok:
                raise Http404()
            else:
                new_account = OJ_account(oj=data[2], username=data[0], password=data[1])
                new_account.save()
                req.user.info.oj_account.add(new_account)
                return HttpResponseRedirect(req.META['HTTP_REFERER'])
        else:
            raise Http404()


@login_required
def sign_up(req):
    if req.method == 'GET':
        update = have_info = wait_review = info_error = reviewed = confirm = over = False
        name = student_id = classes = telephone = qq = None
        user_list = Info.objects.filter(status__gt=2)
        user_number = 100 - len(user_list)
        status = req.user.info.status
        if req.user.info.student_id == 'None' or req.user.info.telephone == 'None' or req.user.info.classes == 'None' or req.user.info.real_name == 'None' or req.user.info.qq == 'None':
            status = 0
            req.user.info.status = 0
            req.user.info.save()
        if status == 0:
            update = True
        elif status == 1:
            have_info = True
        elif status == 2:
            info_error = True
        elif status == 3:
            wait_review = True
        elif status == 4:
            reviewed = True
        elif status == 5:
            confirm = True
        elif status == 6:
            over = True
        if not update:
            name = req.user.info.real_name
            student_id = req.user.info.student_id
            classes = req.user.info.classes
            telephone = req.user.info.telephone
            qq = req.user.info.qq
        try:
            refer = True
            t = req.GET['refer']
        except:
            refer = False
        return render_to_response('sign_up.html', {
            'path': req.path,
            'refer': refer,
            'user_list': user_list,
            'user_number': user_number,
            'update': update,
            'wait_review': wait_review,
            'have_info': have_info,
            'info_error': info_error,
            'reviewed': reviewed,
            'confirm': confirm,
            'over': over,
            'name': name,
            'student_id': student_id,
            'classes': classes,
            'telephone': telephone,
            'qq': qq,
        }, context_instance=RequestContext(req))
    else:
        if req.user.info.status < 4:
            form = SignUpForm(req.POST)
            if form.is_valid():
                form.save(req.user)
        return HttpResponseRedirect(req.META['HTTP_REFERER'])


@login_required
def signing(req):
    if req.META['HTTP_REFERER'][-18:] == "/accounts/sign_up/":
        if req.user.info.status == 1:
            req.user.info.status = 3
            req.user.info.save()
        elif req.user.info.status == 5:
            req.user.info.status = 6
            req.user.info.save()
        return HttpResponseRedirect(req.META['HTTP_REFERER'])
    raise Http404()


@permission_required('auth.change_user')
def accept(req, uid):
    try:
        u = User.objects.get(id=uid)
    except:
        raise Http404()
    if u.info.status == 3:
        u.info.status = 4
        u.info.save()
    return HttpResponseRedirect(req.META['HTTP_REFERER'] + '?refer')


@permission_required('auth.change_user')
def reject(req, uid):
    try:
        u = User.objects.get(id=uid)
    except:
        raise Http404()
    if u.info.status > 3:
        u.info.status = 2
        u.info.save()
    return HttpResponseRedirect(req.META['HTTP_REFERER'] + '?refer')


def test_account(oj, username, password):
    try:
        na = OJ_account.objects.get(oj=oj, username=username, password=password)
    except:
        c = Connect()
        return True if c.test_user(oj, username, password) == '1' else False
    else:
        return False


def updata_user(user):
    c = Connect()
    c.update_user(str(user.info.id))


def updating(req, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404()
    i = 0
    j = 1
    accounts = user.info.oj_account.all()
    for account in accounts:
        if account.is_using:
            i = account.updating
            j = 0
            break
    data = {
        "data": i,
        "over": j
    }
    return JsonResponse(data)


def judge_account(req):
    if req.method == 'GET':
        raise Http404()
    else:
        form = AccountForm(req.POST)
        if form.is_valid():
            data = form.save()
            ret = {}
            ret['data'] = "1" if test_account(data[2], data[0], data[1]) else "0"
            try:
                OJ_account.objects.get(oj=data[2], username=data[0], password=data[1])
            except:
                pass
            else:
                ret['data'] = '0'
            return JsonResponse(ret)
        else:
            return Http404()


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


@permission_required('contest.add_contest')
def clone_contest(req):
    if req.method == 'GET':
        form = CloneContestFrom()
        return render_to_response("clone_contest.html", {
            'form': form,
        }, context_instance=RequestContext(req))
    else:
        form = CloneContestFrom(req.POST)
        if form.is_valid():
            form.save(req.user)
            return HttpResponseRedirect("/")
        else:
            return render_to_response("clone_contest.html", {
                'form': form,
            }, context_instance=RequestContext(req))
