# coding=utf-8
# !/usr/bin/python

from django import template
import datetime

register = template.Library()


@register.tag(name='year')
def do_year(parser, token):
    try:
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError()
    return CurrentTimeNode(format_string[1:-1])
