#coding=utf-8
#!/usr/bin/python

from django import template

register = template.Library()

@register.filter(name='school')
def school(s):
    l = {
        'neau':u'东北农业大学',
        'other':u'其他',
        '':u'',
    }
    return l[s]

@register.filter(name='team')
def team(k):
    if k:
        return 'Yes'
    return 'No'