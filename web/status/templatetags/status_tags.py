# coding=utf-8
#!/usr/bin/python

from django import template

register = template.Library()


@register.filter(name='color')
def color(s):
    key = s[0:7]
    l = {
        'Accepte': 'danger',
        'Wrong A': 'success',
        'Present': 'info',
        'Compila': 'warning',
        'Time Li': 'warning',
        'Memory ': 'warning',
        'Runtime': 'warning',
    }
    return l[key] if l.has_key(key) else ''


@register.filter(name='text_color')
def text_color(s):
    key = s[0:7]
    l = {
        'Accepte': '#CC0000',
        'Wrong A': '#00CC00',
        'Present': '#0000CC',
        'Compila': '#337AB7',
        'Time Li': '#FF6600',
        'Memory ': '#FF6600',
        'Runtime': '#FF6600',
    }
    return l[key] if l.has_key(key) else '#000000'

@register.filter(name='judge_picture')
def judge_picture(s):
    key = s[0:7]
    l = ['Accepte', 'Wrong A', 'Present', 'Compila', 'Time Li', 'Memory ', 'Runtime']
    return '' if key in l else '<img src="/img/loading.gif" width="100%">'