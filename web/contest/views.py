from django.shortcuts import render
from django.shortcuts import render, render_to_response
from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from models import Contest
from forms import AddContestForm
from django import forms
from django.contrib.auth.decorators import login_required, permission_required
import time

# Create your views here.
# 0   ACM
# 1   vjudge
# 2   Student

class ContestForm(forms.Form):
    password = forms.CharField()

    def set_cid(self, cid):
        self.cid = cid

    def clean_password(self):
        password = self.cleaned_data.get("password")
        c = Contest.objects.get(id=self.cid)
        if c.password != password:
            raise forms.ValidationError(message="Error Password!")


def contest_main(req, cid):
    now = time.time()
    cinfo = Contest.objects.get(id=cid)
    type = "<nobr style='color:#CC0033'>Private</nobr>" if cinfo.private else "<nobr style='color:#339933'>Public</nobr>"
    status = "<nobr style='color:#9900CC'>Waiting</nobr>" if time.mktime(cinfo.start_time.timetuple()) > now else (
        "<nobr>Ended</nobr>" if time.mktime(
            cinfo.end_time.timetuple()) < now else "<nobr style='color:#3366FF'>Running</nobr>")
    key = req.session.get('login' + cid, False)
    wait_show = True if time.mktime(cinfo.start_time.timetuple()) > now else False
    if req.user.has_perm('contest.change_contest') or req.user == cinfo.creator:
        key = True
        wait_show = False
    if not key and cinfo.private:
        wait_show = True
    if req.method == 'GET':
        form = ContestForm()
        has_status = req.GET.get('status', 0)
        return render_to_response('contest_main.html', {
            'info': cinfo,
            'type': type,
            'status': status,
            'has_status': has_status,
            'wait_show': wait_show,
            'len': range(len(cinfo.problem.all())),
            'path': req.path,
            'key': key,
            'form': form,
        }, context_instance=RequestContext(req))
    else:
        form = ContestForm(req.POST)
        form.set_cid(cid)
        if form.is_valid():
            req.session['login' + cid] = True
            return HttpResponseRedirect(req.path)
        else:
            return render_to_response('contest_main.html', {
                'info': cinfo,
                'type': type,
                'status': status,
                'wait_show': wait_show,
                'len': range(len(cinfo.problem.all())),
                'path': req.path,
                'key': key,
                'form': form,
            }, context_instance=RequestContext(req))


def add_contest(req, type):
    judge_map = {
        'acm': 0,
        'vjudge': 1,
        'student': 2,
    }
    if type not in ['acm', 'student', 'vjudge'] or req.method == 'GET':
        raise Http404()
    if req.method == 'POST':
        if type in ['acm', 'student'] and not req.user.has_perm('contest.change_contest'):
            raise Http404()
        form = AddContestForm(req.POST)
        if form.is_valid():
            judge_type = judge_map[type]
            form.set_info(req.user, judge_type)
            form.save()
            return HttpResponseRedirect('/contest/' + type + 'list')
        else:
            return render_to_response('contest_add.html', {
                'path': req.path,
                'form': form,
            }, context_instance=RequestContext(req))
    else:
        form = AddContestForm()
        return render_to_response('contest_add.html', {
            'path': req.path,
            'form': form,
        }, context_instance=RequestContext(req))


@permission_required('contest.change_contest')
def hide_contest(req):
    cid = int(req.GET.get('id', 0))
    type = req.GET.get('type', 'acm')
    c = Contest.objects.get(id=cid)
    c.defunct = True
    c.save()
    return HttpResponseRedirect('/contest/' + type + 'list')


@permission_required('contest.change_contest')
def show_contest(req):
    cid = int(req.GET.get('id', 0))
    type = req.GET.get('type', 'acm')
    c = Contest.objects.get(id=cid)
    c.defunct = False
    c.save()
    return HttpResponseRedirect('/contest/' + type + 'list')


def contest_list(req):
    if req.path[9:16] == 'acmlist':
        cinfo = Contest.objects.filter(type=0)
        type = 'ACM'
    elif req.path[9:19] == 'vjudgelist':
        cinfo = Contest.objects.filter(type=1)
        type = 'VJudge'
    elif req.path[9:20] == 'studentlist':
        cinfo = Contest.objects.filter(type=2)
        type = 'Student'
    else:
        raise Http404()
    leng = len(cinfo)
    leng = leng / 20 if leng / 20. == leng // 20 else leng / 20 + 1
    return render_to_response('contest_list.html', {
        'path': req.path,
        'type': type,
        'len': range(leng),
    }, context_instance=RequestContext(req))


def get_contest_info(req, type, page):
    page = int(page)
    first = (page - 1) * 20
    last = page * 20
    data = {'data': ''}
    html = '''
<tr>
    <th scope="row">%s</th>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td%s</td>
    <td%s</td>
    <td>%s</td>

'''
    k = True if req.user.has_perm('change_contest') else False
    if k:
        if req.path[14] == 'a':
            cinfo = Contest.objects.filter(type=0)
        elif req.path[14] == 'v':
            cinfo = Contest.objects.filter(type=1)
        else:
            cinfo = Contest.objects.filter(type=2)
    else:
        if req.path[14] == 'a':
            cinfo = Contest.objects.filter(type=0, defunct=False)
        elif req.path[14] == 'v':
            cinfo = Contest.objects.filter(type=1, defunct=False)
        else:
            cinfo = Contest.objects.filter(type=2, defunct=False)
    last = last if last < len(cinfo) else len(cinfo)
    cinfo = cinfo[first:last]
    ii = (page - 1) * 20 + 1
    now = time.time()
    for i in cinfo:
        s_format = '%Y-%m-%d %H:%M:%S'
        s = html % (
            ii, "<a href='/contest/c/%d#'>%s</a>" % (i.id, i.title), i.start_time.strftime(s_format),
            # i.end_time.strftime(s_format),
            i.end_time - i.start_time,
            " style='color:#CC0033'>Private" if i.private else " style='color:#339933'>Public",
            " style='color:#9900CC'>Waiting" if time.mktime(i.start_time.timetuple()) > now else (
                ">Ended" if time.mktime(i.end_time.timetuple()) < now else " style='color:#3366FF'>Running"), i.creator)
        s += '''<td><a class="btn btn-primary %s" href="/contest/hide/?id=%d&type=%s">H</a></td>
        <td><a class="btn btn-primary %s" href="/contest/show/?id=%d&type=%s">S</a></td></tr>''' % (
            "disabled" if i.defunct else "", i.id, type, "" if i.defunct else "disabled", i.id, type) if k else "</tr>"
        data['data'] += s
        ii += 1
    return JsonResponse(data)


def get_problem(req, cid, pid):
    # cid = int(cid)
    # pid = int(pid)
    data = {}
    now = time.time()
    try:
        cinfo = Contest.objects.get(id=cid)
    except:
        raise Http404()
    key = req.session.get('login' + cid, False)
    wait_show = True if time.mktime(cinfo.start_time.timetuple()) > now else False
    if req.user.has_perm('contest.change_contest') or req.user == cinfo.creator:
        key = True
        wait_show = False
    if not key and cinfo.private:
        wait_show = True
    if not key and wait_show:
        raise Http404()
    pinfo = cinfo.problem.get(problem_new_id=pid)
    data['title'] = pinfo.title
    data['tlc'] = pinfo.problem.time_limit_c
    data['tlj'] = pinfo.problem.time_limit_java
    data['mlc'] = pinfo.problem.memory_limit_c
    data['mlj'] = pinfo.problem.memory_limit_java
    data['description'] = pinfo.problem.description
    data['input'] = pinfo.problem.input
    data['output'] = pinfo.problem.output
    data['sinput'] = pinfo.problem.sample_input
    data['soutput'] = pinfo.problem.sample_output
    data['hint'] = pinfo.problem.hint
    data['source'] = pinfo.problem.source
    return JsonResponse(data)


def f_cmp(x, y):
    return int(y[0].id - x[0].id)


def get_status(req, cid, page):
    data = {}
    now = time.time()
    try:
        cinfo = Contest.objects.get(id=cid)
    except:
        raise Http404()
    page = int(page)
    if page <= 0:
        raise Http404()
    key = req.session.get('login' + cid, False)
    wait_show = True if time.mktime(cinfo.start_time.timetuple()) > now else False
    if req.user.has_perm('contest.change_contest') or req.user == cinfo.creator:
        key = True
        wait_show = False
    if not key and cinfo.private:
        wait_show = True
    if not key and wait_show:
        raise Http404()
    s = []
    for i in cinfo.problem.all():
        for j in i.status.all():
            # if j.submit_time > cinfo.start_time and j.submit_time < cinfo.end_time:
            s.append((j, i.title))
    data['len'] = len(s)
    data['status'] = []
    s.sort(cmp=f_cmp)
    if page < 1 or page > data['len'] / 20 + 1:
        data['error'] = 1
    else:
        data['error'] = 0
        s = s[(page - 1) * 20:page * 20]
        data['first'] = 0 if (page - 1) * 20 else 1
        data['last'] = 0 if page * 20 < data['len'] else 1
        for i in s:
            data['status'].append([i[0].id, i[0].submit_time, i[0].status, i[0].problem.oj, i[1], i[0].use_time, i[0].use_memory, i[0].length, i[0].language, i[0].user.username])
    return JsonResponse(data)
