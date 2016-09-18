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
    key = s[0:8]
    l = {
        'Accepted': '#CC0000',
        'Wrong An': '#009900',
        'Presenta': '#0000CC',
        'Compilat': '#337AB7',
        'Time Lim': '#FF6600',
        'Memory L': '#FF6600',
        'Runtime ': '#FF6600',
        'Output L': '#FF6600'
    }
    return l[key] if key in l else '#000000'

@register.filter(name='judge_picture')
def judge_picture(s):
    key = s[0:8]
    l = ['Accepted', 'Wrong An', 'Presenta', 'Compilat', 'Time Lim', 'Memory L', 'Runtime ', 'Output L', 'Judge ER']
    return '' if key in l else '<img src="/img/loading.gif" width="100%">'