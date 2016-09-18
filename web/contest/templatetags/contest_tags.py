# coding=utf-8
# !/usr/bin/python

from django import template

register = template.Library()


@register.filter(name='problem_list')
def problem_list(i):
    i = int(i)
    s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return s[i]
