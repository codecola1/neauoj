__author__ = 'Code_Cola'

from django import forms
from contest.models import Contest
import time
import json


class AddContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ('title', 'start_time', 'end_time', 'description', 'password', 'creator')

    def save(self, commit=True):
        pass


class AddVudgeForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ('title', 'start_time', 'end_time', 'description', 'password')

    data = forms.CharField()

    def set_creator(self, user):
        self.user = user

    def clean_data(self):
        data = self.cleaned_data.get("data")
        try:
            data = json.dumps(data)
        except:
            raise forms.ValidationError(message="")
        else:
            return data

    def clean_start_time(self):
        start_time = self.cleaned_data.get("start_time")
        print type(start_time)
        try:
            start_time = time.strptime(start_time, "%Y-%m-%d %H:%M")
        except:
            raise forms.ValidationError(message="")
        else:
            return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data.get("end_time")
        try:
            end_time = time.strptime(end_time, "%Y-%m-%d %H:%M")
        except:
            raise forms.ValidationError(message="")

    def save(self, commit=True):
        self.start_time = self.cleaned_data.get("start_time")
        print self.start_time
        return ""
