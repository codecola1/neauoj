#coding=utf-8
#!/usr/bin/python

from django import forms

class UserForm(forms.Form):
	username = forms.CharField(label = '用户名', max_length = 50)
	password = forms.CharField(label = '密码', widget = forms.PasswordInput())