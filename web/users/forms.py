# coding=utf-8
# !/usr/bin/python

from django.contrib.auth.models import User, Permission
from users.models import Info
from django import forms
from web.connect import Connect
import re


class UserRegisterForm(forms.ModelForm):
    error_messages = {
        'username_mismatch': ("The Username can only fill in the letters, numbers and underscodes."),
        'username_mismatch_have': ("Users have been registered."),
        'password_mismatch': ("The two password fields didn't match."),
        'school_mismatch': ("School can not be empty."),
        'grade_mismatch': ("Grade can not be empty."),
    }
    school_choice = (
        (u'', u'School'),
        (u'neau', u'东北农业大学'),
        (u'others', u'其他'),
    )
    grade_choice = [(u'', u'Grade')]
    grade_choice.extend([(unicode(year), unicode(year)) for year in range(2010, 2017)])
    username = forms.CharField(
            error_messages={'required': 'Your username is Required'}
    )
    email = forms.EmailField(error_messages={'required': 'Your email is Required'})
    password1 = forms.CharField(error_messages={'required': 'Your password is Required'})
    password2 = forms.CharField(error_messages={'required': 'Your password confirmation is Required'})
    school = forms.ChoiceField(
            error_messages={'required': 'Your school is Required'},
            choices=school_choice,
            widget=forms.Select(attrs={'class': 'form-control'})
    )
    grade = forms.ChoiceField(
            error_messages={'required': 'Your grade is Required'},
            choices=grade_choice,
            widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Info
        fields = ("nickname", "school", "grade")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        ma = re.match('^[a-zA-Z0-9_]+$', username)
        if not ma:
            raise forms.ValidationError(
                    self.error_messages['username_mismatch'],
                    code='username_mismatch',
            )
        try:
            u = User.objects.get(username=username)
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
            school = u"东北农业大学"
        return school

    def clean_grade(self):
        grade = self.cleaned_data.get("grade")
        if not grade or not grade.isdigit():
            grade = "2016"
        return grade

    def save(self, commit=True):
        # user = super(UserRegisterForm, self).save(commit=False)
        username = self.cleaned_data.get("username")
        nickname = self.cleaned_data.get("nickname")
        email = self.cleaned_data.get("email")
        school = self.cleaned_data.get("school")
        grade = self.cleaned_data.get("grade")
        user = User(username=username, email=email)
        user.set_password(self.cleaned_data["password2"])
        user.save()
        info = Info(user=user, nickname=nickname, school=school, grade=grade)
        info.save()
        return user


class PermissionForm(forms.Form):
    username = forms.CharField()
    permission = forms.ChoiceField(
            choices=(
                ('1', 'Can add permission'),
                ('8', 'Can change user'),
                ('43', 'Can add problem'),
                ('47', 'Can change solve'),
                ('40', 'Can add Contest'),
            )
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            User.objects.get(username=username)
        except:
            raise forms.ValidationError(
                    "No such User",
                    code='username_mismatch',
            )
        return username

    def save(self):
        username = self.cleaned_data.get("username")
        permission = self.cleaned_data.get("permission")
        u = User.objects.get(username=username)
        p = Permission.objects.get(id=permission)
        u.user_permissions.add(p)


class ChangePasswd(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    def set_user(self, user):
        self.this_user = user
        self.permission = user.has_perm('change_user')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            self.user = User.objects.get(username=username)
        except:
            raise forms.ValidationError(
                    "No such User",
                    code='username_mismatch',
            )
        if not self.permission and self.user != self.this_user:
            raise forms.ValidationError(
                    "Access denied!",
                    code='username_mismatch',
            )
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if not self.permission and not self.user.check_password(password1):
            raise forms.ValidationError(
                    "Incorrect password!",
                    code='password_mismatch',
            )
        return password2

    def save(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password2')
        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()


class AddUserForm(forms.Form):
    pass


class SignUpForm(forms.Form):
    name = forms.CharField()
    student_id = forms.CharField()
    classes = forms.CharField()
    telephone = forms.CharField()
    qq = forms.CharField()

    def clean_student_id(self):
        student_id = self.cleaned_data.get("student_id")
        ma = re.match('^[0-9]{8}$', student_id)
        if not ma:
            student_id = "None"
        return student_id

    def clean_telephone(self):
        telephone = self.cleaned_data.get("telephone")
        ma = re.match('^[0-9]{11}$', telephone)
        if not ma:
            telephone = "None"
        return telephone

    def clean_qq(self):
        qq = self.cleaned_data.get("qq")
        ma = re.match('^[0-9]+$', qq)
        if not ma:
            qq = "None"
        return qq

    def save(self, user):
        name = self.cleaned_data.get("name")
        student_id = self.cleaned_data.get("student_id")
        classes = self.cleaned_data.get("classes")
        telephone = self.cleaned_data.get("telephone")
        qq = self.cleaned_data.get("qq")

        user.info.real_name = name
        user.info.student_id = student_id
        user.info.classes = classes
        user.info.telephone = telephone
        user.info.qq = qq
        user.info.status = 1
        user.info.save()


class EditInforForm(forms.Form):
    username = forms.CharField()
    nickname = forms.CharField()
    password = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            self.user = User.objects.get(username=username)
        except:
            raise forms.ValidationError(
                    "No such User",
                    code='username_mismatch',
            )
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError(
                    "Incorrect password!",
                    code='password_mismatch',
            )
        return password

    def save(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        nickname = self.cleaned_data.get("nickname")
        u = User.objects.get(username=username)
        u.info.nickname = nickname
        u.info.save()


class AccountForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    oj = forms.CharField()

    def save(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        oj = self.cleaned_data.get("oj")

        return [username, password, oj.lower()]


class CloneContestFrom(forms.Form):
    cid = forms.IntegerField()

    def clean_cid(self):
        cid = self.cleaned_data.get("cid")
        c = Connect()
        number = int(c.test_contest(cid))
        if number == 0:
            raise forms.ValidationError("No Such Contest")
        self.number = number
        return cid

    def save(self, user):
        cid = self.cleaned_data.get("cid")
        from datetime import datetime
        from problem.models import Problem
        from contest.models import Contest, In_Problem

        try:
            contest = Contest.objects.get(clone=cid)
            flag = True
        except:
            contest = Contest(
                    title="None",
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    description="",
                    private=0,
                    impose=0,
                    type=1,
                    password="",
                    creator=user,
            )
            contest.save()
            flag = False
        if not flag:
            for i in range(self.number):
                p = Problem(oj="hdu_std", problem_id=i + 1001, judge_type=1, data_number=cid)
                p.save()
                new_problem = In_Problem(
                        problem=p,
                        problem_new_id=i,
                        title="None",
                )
                new_problem.save()
                contest.problem.add(new_problem)
        c = Connect()
        c.clone_contest(cid, contest.id)
