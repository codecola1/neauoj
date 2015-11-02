from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User, Permission
from django import forms
from problem.robot.get_problem import Down_problem


# Create your views here.

def index(req):
    if req.method == 'GET':
        return render_to_response('index.html', {
            'path': req.path,
        }, context_instance=RequestContext(req))


class testform(forms.Form):
    oj = forms.ChoiceField(
        choices=(('hdu', 'hdu'), ('poj', 'poj'))
    )
    ind = forms.IntegerField()


def test(req):
    if req.method == 'POST':
        form = testform(req.POST)
        if form.is_valid():
            ind = form.cleaned_data['ind']
            oj = form.cleaned_data['oj']
            test = Down_problem(oj, ind)
            if test.right:
                test.get_info()
                test.get_img()
            # for i in range(ind, ind + 10):
            #     test = Down_problem(oj, i)
            #     if test.right:
            #         test.get_info()
            #         test.get_img()
        return render_to_response('test.html', {
            'form': form,
            'pname': test.pid,
            'title': test.Title if test.right else "",
            'description': test.Description if test.right else "",
            'input': test.Input if test.right else "",
            'output': test.Output if test.right else "",
            'sinput': test.Sinput if test.right else "",
            'soutput': test.Soutput if test.right else "",
            'hint': test.Hint if test.right else "",
            'author': test.Source if test.right else "",
        }, context_instance=RequestContext(req))
    else:
        form = testform()
        return render_to_response('test.html', {
            'path': req.path,
            'form': form,
            'pname': 'None',
            'title': '',
            'description': '',
            'input': '',
            'output': '',
            'sinput': '',
            'soutput': '',
            'hint': '',
            'author': '',
        }, context_instance=RequestContext(req))