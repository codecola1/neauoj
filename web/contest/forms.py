__author__ = 'Code_Cola'

from django import forms
from contest.models import Contest


class AddContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ('title', 'start_time', 'end_time', 'description', 'password', 'creator')

    def save(self, commit=True):
        pass