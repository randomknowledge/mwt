from django.conf import settings
from datetime import datetime
import pytz


def get_tz(tzstring=None):
    if not tzstring:
        tzstring = getattr(settings, 'TIME_ZONE', 'UTC')
    return pytz.timezone(tzstring)


def get_tznow(tzstring=None):
    return datetime.now(tz=get_tz(tzstring=tzstring))