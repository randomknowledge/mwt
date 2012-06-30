from django import template
from django.utils.text import wrap

register = template.Library()


@register.filter
def hardwrap(text, line_length):
    return '\n'.join([add_spaces(t, line_length) for t in text.split('\n')])


@register.filter
def subtract(value, arg):
    return value - arg


def add_spaces(text, line_length):
    if len(text) <= line_length:
        return text

    i = 0
    l = len(text)
    t = ''
    while i < l:
        t = t + text[i:i + line_length] + ' '
        i = i + line_length
    return t