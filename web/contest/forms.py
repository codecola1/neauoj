__author__ = 'Code_Cola'

from django import forms
from contest.models import Contest, In_Problem
from problem.models import Problem
import datetime
import time
import json


class AddContestForm(forms.ModelForm):
    problem_data = forms.CharField()
    contest_title = forms.CharField()

    class Meta:
        model = Contest
        fields = ('start_time', 'end_time', 'description', 'password')

    def set_info(self, user, judge_type):
        self.user = user
        self.judge_type = judge_type

    def clean_problem_data(self):
        problem_data = self.cleaned_data.get("problem_data")
        self.problem = []
        try:
            problem_data = json.loads(problem_data)
        except:
            raise forms.ValidationError(message="")
        for i in problem_data['problems']:
            if i:
                try:
                    problem = Problem.objects.get(id=i)
                except:
                    raise forms.ValidationError(message="")
                else:
                    self.problem.append(problem)
        return problem_data

    def clean_start_time(self):
        start_time = self.cleaned_data.get("start_time")
        # print type(start_time)
        # try:
        #     start_time = time.strptime(start_time, "%Y-%m-%d %H:%M")
        # except:
        #     raise forms.ValidationError(message="")
        # else:
        return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data.get("end_time")
        start_time = self.cleaned_data.get("start_time")
        if end_time < start_time:
            raise forms.ValidationError(message="")
        return end_time

    def save(self, commit=True):
        title = self.cleaned_data.get("contest_title")
        description = self.cleaned_data.get("description")
        password = self.cleaned_data.get("password")
        private = 1 if password else 0
        start_time = self.cleaned_data.get("start_time")
        end_time = self.cleaned_data.get("end_time")
        problem_data = self.cleaned_data.get("problem_data")
        contest = Contest(
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description,
            private=private,
            impose=0,
            type=self.judge_type,
            password=password,
            creator=self.user,
        )
        contest.save()
        for i in range(0, problem_data['number']):
            title = problem_data['titles'][i]
            if not title:
                title = self.problem[i].title
            new_problem = In_Problem(
                problem=self.problem[i],
                problem_new_id=i,
                title=title,
            )
            new_problem.save()
            contest.problem.add(new_problem)
        return contest
