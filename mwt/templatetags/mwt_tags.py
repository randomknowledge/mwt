import re
import math
from django import template
from django.core.urlresolvers import reverse
from .. import constants


register = template.Library()


@register.simple_tag
def run_admin_url(id, fill_length=0):
    url = constants.MWT_SETTINGS.get('url') + reverse('admin:mwt_testrun_change', args=[id])
    if fill_length == 0:
        return url
    return fill(url, "%s, ,,right" % fill_length)


@register.filter
def hardwrap(text, line_length):
    return '\n'.join([interject_string(t, line_length) for t in text.split('\n')])


@register.filter
def hardwrap_and_fillright(text, args):
    line_length, fill_length, char = args.split(',')

    txt = ''
    for line in text.split('\n'):
        line = interject_string(line, line_length, "\n").split('\n')
        for l in line:
            l = fill(l, "%s, ,,right" % fill_length) + char
            txt += l + "\n"
    return txt.rstrip()


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def lineprepend(value, char):
    return "\n".join([char + v for v in value.split("\n")])


@register.filter
def fill(value, args):
    value = unicode(value)
    args = args.split(',')
    num = int(args[0])
    char = args[1] or ' '
    wrap = args[2] or ''
    type = args[3]
    if type != 'center' and type != 'left' and type != 'right':
        type = 'center'

    value = wrap + value + wrap

    if len(value) >= num:
        return value

    if type == 'center':
        left = int(math.ceil((num - len(value)) / 2))
        right = int(math.floor((num - len(value)) / 2))
        for i in range(0, left):
            value = char + value
        for i in range(0, right):
            value += char
    else:
        while len(value) < num:
            if type == 'left':
                value = char + value
            else:
                value += char
    return value


@register.filter
def fill_lines(value, args):
    args = args.split(',')
    char = args.pop() + '\n'
    args = ','.join(args)
    return char.join([fill(t, args) for t in value.split('\n')])


def interject_string(text, line_length, char=' '):
    line_length = int(line_length)
    if len(text) <= line_length:
        return text

    i = 0
    l = len(text)
    t = ''
    while i < l:
        t = t + text[i:i + line_length] + char
        i = i + line_length
    return re.sub(r'\n$', '', t)
