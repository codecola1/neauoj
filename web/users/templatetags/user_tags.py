# coding=utf-8
# !/usr/bin/python

from django import template

register = template.Library()


@register.filter(name='school')
def school(s):
    l = {
        'neau': u'东北农业大学',
        'others': u'其他',
        '': u'',
    }
    return l[s]


@register.filter(name='team')
def team(k):
    if k:
        return 'Yes'
    return 'No'


@register.filter(name='sign_span')
def sign_span(i):
    span_list = ['danger', 'danger', 'warning', 'info', 'primary', 'info', 'success']
    return span_list[i]


@register.filter(name='sign_text')
def sign_text(i):
    text_list = ['未报名', '未报名', '未通过', '待审核', '审核通过', '待确认', '报名成功']
    return text_list[i]
