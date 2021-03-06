from django.template.loader import render_to_string
from django.utils.safestring import SafeUnicode

try:
    from announce.templatetags import announcetags
except Exception:
    pass
import re
import math
from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ungettext
from .. import constants
from ..models.abstract import Plugin
from ..models.base import Client, Website


register = template.Library()

@register.simple_tag
def re_replace(string, pattern, replace):
    return re.sub(pattern, replace, string)


@register.filter
def concat(value, c):
    return "%s%s" % (value, c)


@register.simple_tag
def boolean_button(active=False, button_id=None, classes=None):
    return render_to_string("mwt/main/snippets/boolean_button.html", {'active': active, 'id': button_id, 'classes': classes})


@register.simple_tag
def get_testrun_filter_url(obj, request):
    path = request.META.get('PATH_INFO')

    get = request.GET.copy()
    if 'filterby' in get:
        get.pop('filterby')
    if 'filterid' in get:
        get.pop('filterid')

    filterby = 'test'
    if isinstance(obj, Plugin):
        filterby = 'plugin'
    elif isinstance(obj, Client):
        filterby = 'client'
    elif isinstance(obj, Website):
        filterby = 'website'

    if type(obj) == dict and 'type' in obj and 'key' in obj:
        filterby = obj.get('type')
        id = obj.get('key')
    elif isinstance(obj, SafeUnicode) or type(obj) == str:
        id = ''
    else:
        id = obj.pk

    if obj:
        get.update({
            'filterby': filterby,
            'filterid': id,
        })
    return '%s?%s' % (path, get.urlencode())


@register.simple_tag
def testrun_filter_active_class(filterby, request):
    if request.GET.get('filterby', '') == filterby:
        return 'active'
    return ''


@register.simple_tag
def mwt_announce_js():
    if constants.MWT_SETTINGS.get('use_nodejs'):
        try:
            return announcetags.announce_js()
        except Exceptione:
            pass
    return ''


@register.filter
def format_timedelta(delta):
    num_years = delta.days / 365
    if num_years > 0:
        return ungettext(u"%d year", u"%d years", num_years) % num_years

    num_weeks = delta.days / 7
    if num_weeks > 0:
        return ungettext(u"%d week", u"%d weeks", num_weeks) % num_weeks

    if delta.days > 0:
        return ungettext(u"%d day", u"%d days", delta.days) % delta.days

    num_hours = delta.seconds / 3600
    num_minutes = delta.seconds / 60

    if num_hours > 0:
        minutes = num_minutes - num_hours * 60
        str_minutes = ungettext(u"%d minute", u"%d minutes", minutes) % minutes
        return ungettext(u"%d hour %s", u"%d hours %s", (num_hours, str_minutes)) % (num_hours, str_minutes)

    if num_minutes > 0:
        s_seconds = delta.seconds - num_minutes * 60
        str_seconds = ungettext(u"%d second", u"%d seconds", s_seconds) % s_seconds
        return ungettext(u"%d minute %s", u"%d minutes %s", (num_minutes, str_seconds)) % (num_minutes, str_seconds)

    seconds = delta.seconds + delta.microseconds / 1000000.0
    return ungettext(u"%2.2f seconds", u"%2.2f seconds", seconds) % seconds


@register.simple_tag
def run_admin_url(id, fill_length=0):
    url = constants.MWT_SETTINGS.get('url') + reverse('admin:mwt_testrun_change', args=[id])
    if fill_length == 0:
        return url
    return fill(url, "%s, ,,right" % fill_length)


@register.filter
def ucfirst(text):
    return text[0].upper() + text[1:]


@register.filter
def state_to_bootstrap(state):
    return {
        constants.RUN_STATUS_FAIL: 'important',
        constants.RUN_STATUS_PENDING: 'info',
        constants.RUN_STATUS_RUNNING: 'warning',
        constants.RUN_STATUS_SUCCESS: 'success',
        'false': 'important',
        'true': 'success',
    }.get(str(state).lower())


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
