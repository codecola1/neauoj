__author__ = 'Code_Cola'

from django import forms
from models import Solve
from problem.models import Problem
from django.contrib.auth.models import User


class SubmitForm(forms.ModelForm):
    error_messages = {
        'code': 'Code is too short',
        'language': "Language can not be empty",
        'problem': "Not such problem",
    }

    language_choice = (
        (u'', u'Language'),
        (u'c', u'C'),
        (u'c++', u'C++'),
        (u'java', u'Java'),
    )

    language = forms.ChoiceField(
        error_messages={'required': 'Language can not be empty'},
        choices=language_choice,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    problem = forms.CharField()
    uid = forms.CharField()

    class Meta:
        model = Solve
        fields = ('language', 'code')

    def clean_problem(self):
        problem_id = self.cleaned_data.get("problem")
        try:
            Problem.objects.get(id=problem_id)
        except:
            raise forms.ValidationError(
                self.error_messages['problem'],
                code='problem_error'
            )
        return problem_id

    def clean_code(self):
        code = self.cleaned_data.get("code")
        if len(code) < 50 or len(code) >= 65536:
            raise forms.ValidationError(
                self.error_messages['code'],
                code='code_error'
            )
        return code

    def clean_language(self):
        language = self.cleaned_data.get("language")
        if not language or language == 'Language':
            raise forms.ValidationError(
                self.error_messages['language'],
                code='language_error'
            )
        return language

    def save(self, commit=True):
        problem_id = self.cleaned_data.get("problem")
        language = self.cleaned_data.get("language")
        code = self.cleaned_data.get("code")
        uid = self.cleaned_data.get("uid")
        p = Problem.objects.get(id=problem_id)
        u = User.objects.get(id=uid)
        solve = Solve(user=u, problem=p, language=language, code=code, wait_show=True, length=len(code))
        solve.save()
        return solve