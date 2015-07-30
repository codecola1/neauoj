#coding=utf-8
#!/usr/bin/python

from django.contrib.auth.models import User
from users.models import Info
from django import forms
import re

class UserRegisterForm(forms.ModelForm):
    error_messages = {
        'username_mismatch': ("The Username can only fill in the letters, number and underscode."),
        'username_mismatch_have': ("Users have been registered."),
        'password_mismatch': ("The two password fields didn't match."),
        'school_mismatch' : ("School can not be empty."),
        'grade_mismatch' : ("Grade can not be empty."),
    }
    school_choice = (
        (u'', u'School'),
        (u'neau',u'东北农业大学'),
        (u'others',u'其他'),
    )
    grade_choice = [(u'', u'Grade')]
    grade_choice.extend([(unicode(year),unicode(year)) for year in range(2010, 2016)])
    username = forms.CharField(
        error_messages={'required': 'Your username is Required'}
    )
    email = forms.EmailField(error_messages={'required': 'Your email is Required'})
    password1 = forms.CharField(error_messages={'required': 'Your password is Required'})
    password2 = forms.CharField(error_messages={'required': 'Your password confirmation is Required'})
    school = forms.ChoiceField(
        error_messages={'required': 'Your school is Required'},
        choices=school_choice,
        widget=forms.Select(attrs={'class':'form-control'})
    )
    grade = forms.ChoiceField(
        error_messages={'required': 'Your grade is Required'},
        choices=grade_choice,
        widget=forms.Select(attrs={'class':'form-control'})
    )


    class Meta:
        model = Info
        fields = ("nickname","school","grade")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        ma = re.match('^[a-zA-Z0-9_]+$', username)
        if not ma:
            raise forms.ValidationError(
                self.error_messages['username_mismatch'],
                code='username_mismatch',
            )
        try:
            u = User.objects.get(username = username)
        except:
            return username
        else:
            raise forms.ValidationError(
                self.error_messages['username_mismatch_have'],
                code='username_mismatch_have',
            )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_school(self):
        school = self.cleaned_data.get("school")
        if not school or school == 'School':
            raise forms.ValidationError(
                self.error_messages['school_mismatch'],
                code='school_mismatch',
            )
        return school

    def clean_grade(self):
        grade = self.cleaned_data.get("grade")
        if not grade or not grade.isdigit():
            raise forms.ValidationError(
                self.error_messages['grade_mismatch'],
                code='grade_mismatch',
            )
        return grade

    def save(self, commit=True):
        # user = super(UserRegisterForm, self).save(commit=False)
        username = self.cleaned_data.get("username")
        nickname = self.cleaned_data.get("nickname")
        email = self.cleaned_data.get("email")
        school = self.cleaned_data.get("school")
        grade = self.cleaned_data.get("grade")
        user = User(username = username, email = email)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        info = Info(user = user, nickname = nickname, school = school, grade = grade)
        info.save()
        return user